import os
import sys
import glob
import json
import argparse
import validators
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import NLTKTextSplitter, SpacyTextSplitter, CharacterTextSplitter

from dotenv import load_dotenv

load_dotenv()

import pprint
pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser()
parser.add_argument('document', type=str)
parser.add_argument('--splitter', type=str, choices=["sentence", "token"], default="sentence")
args = parser.parse_args()

document_type = None
if validators.url(args.document):
    if "youtube" in args.document:
        document_type = "DOCUMENT_TYPE_YOUTUBE"
    else:
        document_type = "DOCUMENT_TYPE_URL"
elif args.document.endswith('txt'):
    document_type = "DOCUMENT_TYPE_TXT"
elif args.document.endswith('PDF'):
    document_type = "DOCUMENT_TYPE_PDF"
elif args.document.endswith('HTML'):
    document_type = "DOCUMENT_TYPE_HTML"
else:
    print("unsupported document type")
    sys.exit(1)

# CHUNKS TO PUT IN JSON
chunks = []

if args.splitter == "sentence":
    text_splitter = NLTKTextSplitter(chunk_size=1000)  # use this for everything if you can
    # text_splitter = SpacyTextSplitter(chunk_size=1000)
elif args.splitter == "token":
    # use this if we can't get small enough chunks
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=100)
else:
    print("unsupported splitter type")
    sys.exit(1)

# HTML (aka EPUB)
if document_type == "DOCUMENT_TYPE_HTML":
    from langchain.document_loaders import UnstructuredHTMLLoader
    loader = UnstructuredHTMLLoader(args.document)
    data = loader.load()
    texts = text_splitter.split_text(data[0].page_content)
    for text in texts:
        chunks.append(
            {"source": args.document, "content": text}
        )

# SPLIT PDFS
elif document_type == "DOCUMENT_TYPE_PDF":
    from langchain.document_loaders import PagedPDFSplitter
    pdf_uri = args.document
    loader = PagedPDFSplitter(pdf_uri)
    pages = loader.load_and_split()

    for page in pages:
        texts = text_splitter.split_text(page.page_content)
        for text in texts:
            chunks.append(
                {"source": pdf_uri, "content": text}
            )

# SCRAPE FROM URL
elif document_type == "DOCUMENT_TYPE_PDF":
    urls = [
        # google rework
        # "https://rework.withgoogle.com/print/guides/5749328048029696/",
        # "https://rework.withgoogle.com/print/guides/5383427704487936/",
        # "https://rework.withgoogle.com/print/guides/5699257587728384/",
        # "https://rework.withgoogle.com/print/guides/5083289484263424/",
        # "https://rework.withgoogle.com/print/guides/5989177275449344/",
        # "https://rework.withgoogle.com/print/guides/5730082031140864/",
        # "https://rework.withgoogle.com/print/guides/5664902681198592/",
        # "https://rework.withgoogle.com/print/guides/6309005504806912/",
        # "https://rework.withgoogle.com/case-studies/CalGovOps-manager-training/",
        # "https://rework.withgoogle.com/blog/the-evolution-of-project-oxygen/",
        # "https://rework.withgoogle.com/blog/listen-to-this-podcast-on-how-Google-develops/",
        # "https://rework.withgoogle.com/blog/support-managers-with-rework-tools/",
        # "https://rework.withgoogle.com/blog/Googles-effort-to-make-managers-awesome/",
        # "https://rework.withgoogle.com/blog/rework-for-small-businesses/",

        # code climate
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/7-biggest-communication-problems-facing-remote-engineering-teams",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/abandoned-pull-requests",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/achieve-continuous-delivery-with-velocity-metrics",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/be-a-proactive-engineering-leader",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/cd-is-a-culture",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/combat-performance-review-biases-with-objective-data",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/continuous-delivery-best-practices",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/continuous-delivery-pipeline-deployment-blockers",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/cto-and-ceo-alignment",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/culture-of-feedback-engineering",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/data-driven-engineering-leadership",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/data-driven-performance-reviews",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/dora-metrics",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/engineering-knowledge-silos",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/engineering-kpis-board-deck",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/engineering-leaders-business-language",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/engineering-metrics-are-business-metrics",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/engineering-success-beyond-the-sprint",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/how-to-identify-bottlenecks-engineering",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/how-to-unblock-engineers-and-boost-engineering-productivity",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/introducing-the-engineering-leaders-guide-to-data-driven-leadership",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/metrics-manage-large-team",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/moneyball-engineering-metrics",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/most-impactful-software-metrics",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/performance-reviews",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/plan-retrospectives-with-data",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/prepare-for-standups",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/productive-scrum-retrospectives",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/productive-standup-meeting",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/rework-costs-millions",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/roll-out-engineering-metrics",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/run-effective-retros-data",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/run-impactful-standups",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/scale-engineering-calculator",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/software-engineering-cycle-time",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/step-up-your-standups",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/stop-asking-developers-three-standup-questions",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/stop-code-review-bottlenecking",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/stop-micromanaging-team",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/the-engineering-intelligence-managers-need-is-now-free-forever",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/the-essential-data-for-leading-a-remote-engineering-team",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/the-fallacy-of-process",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/the-space-framework",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/three-questions-standup-part-ii",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/time-wasting-code-review",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/upskilling-engineering-teams",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/using-data-psychological-safety",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/using-data-to-coach-ics",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/using-velocity-to-identify-patterns-of-top-performing-teams",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/virtuous-circle-software-delivery",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/what-data-science-tells-us-about-shipping-faster",
        # "https://cod-twister-production.cl-us-east-3.servd.dev/blog/you-cant-set-effective-goals-for-software-developers-without-data",
        # "https://codeclimate.com/blog/competency-vs-productivity",
        # "https://codeclimate.com/blog/deployment-frequency",
        # "https://codeclimate.com/blog/improve-engineering-team-health",
        # "https://codeclimate.com/blog/maintaining-alignment-with-stakeholders",

        # faros (embedded)
        # "https://www.faros.ai/blog/shocking-results-or-not-so-from-the-state-of-devops-2022-survey",
        # "https://www.faros.ai/blog/its-time-to-do-more-with-less",
        # "https://www.faros.ai/blog/are-you-using-or-about-to-use-dora-metrics-read-this-first",
        # "https://www.faros.ai/blog/value-stream-management-in-software",
        # "https://www.faros.ai/blog/sprint-velocity-what-it-is-and-what-it-is-not",
        # "https://www.faros.ai/blog/lead-time-for-software-delivery",
        # "https://www.faros.ai/blog/all-you-need-to-know-about-the-dora-metrics-and-how-to-measure-them",

        # haystack blog posts (embedded)
        # "https://www.usehaystack.io/blog/measuring-devops-beyond-dora-accelerate-metrics",
        # "https://www.usehaystack.io/blog/managing-with-metrics-a-guide-for-engineering-managers",
        # "https://www.usehaystack.io/blog/7-jira-delivery-metrics-for-software-dev-teams",
        # "https://www.usehaystack.io/blog/lead-time-cycle-time-change-lead-time",
        # "https://www.usehaystack.io/blog/engineering-productivity-engprod-the-secret-of-elite-developer-teams",
        # "https://www.usehaystack.io/blog/83-of-developers-suffer-from-burnout-haystack-analytics-study-finds",
        # "https://www.usehaystack.io/blog/ship-software-smaller-deliver-better-product",
        # "https://www.usehaystack.io/blog/developers-defensive-culture-psychological-safety",
        # "https://www.usehaystack.io/blog/haystack-analytics-attracts-investment-powering-engineering-teams-globally-and-addresses-developer-burnout",
        # "https://www.usehaystack.io/blog/are-project-micromanagement-tools-harmful",
        # "https://www.usehaystack.io/blog/managing-developers-measure-dont-micromanage",
        # "https://www.usehaystack.io/blog/are-you-using-harmful-software-engineering-metrics",
        # "https://www.usehaystack.io/blog/the-accelerate-book-the-four-key-devops-metrics-why-they-matter",
        # "https://www.usehaystack.io/blog/the-true-cost-of-context-switching",
        # "https://www.usehaystack.io/blog/beginners-guide-to-software-delivery-metrics",
        # "https://www.usehaystack.io/blog/does-engineering-performance-drive-profitability-heres-what-the-data-says",
        # "https://www.usehaystack.io/blog/software-delivery-survey-template",
        # "https://www.usehaystack.io/blog/4-step-guide-to-improving-software-delivery",
        # "https://www.usehaystack.io/blog/what-makes-a-successful-engineering-team",
        # "https://www.usehaystack.io/blog/5-steps-for-giving-developer-feedback",
        # "https://www.usehaystack.io/blog/cycle-time-reduction-beginners-guide-to-reducing-cycle-time",
        # "https://www.usehaystack.io/blog/we-cancelled-standups-and-let-the-team-build-heres-what-happened",
        # "https://www.usehaystack.io/blog/software-developer-burnout-how-to-spot-early-warning-signs",
        # "https://www.usehaystack.io/blog/software-development-metrics-pros-cons-and-why-past-attempts-have-failed",
        # "https://www.usehaystack.io/blog/using-git-to-identify-blockers-before-its-too-late",
        # "https://www.usehaystack.io/blog/software-development-metrics-top-5-commonly-misused-metrics",
        # "https://www.usehaystack.io/blog/software-development-metrics-measuring-what-matters-2",

        # swarmia (embedded already)
        # "https://www.swarmia.com/blog/developer-experience-what-why-how/",
        # "https://www.swarmia.com/blog/size-age-culture-productivity/",
        # "https://www.swarmia.com/blog/continuous-improvement-in-software-development/",
        # "https://www.swarmia.com/blog/daily-stand-ups/",
        # "https://www.swarmia.com/blog/velocity-vs-cycle-time/",
        # "https://www.swarmia.com/blog/space-framework/",
        # "https://www.swarmia.com/blog/dora-change-failure-rate/",
        # "https://www.swarmia.com/blog/balancing-engineering-investments/",
        # "https://www.swarmia.com/blog/ship-software-10x-faster/",
        # "https://www.swarmia.com/blog/product-development-performance-for-investors/",
        # "https://www.swarmia.com/blog/dora-metrics/",
        # "https://www.swarmia.com/blog/software-engineers-learn-on-company-time/",
        # "https://www.swarmia.com/blog/issue-cycle-time/",
        # "https://www.swarmia.com/blog/agile-team-working-agreements/",
        # "https://www.swarmia.com/blog/measuring-software-development-productivity/",
        # "https://www.swarmia.com/blog/data-driven-retrospectives-stop-fake-improvements/",
        # "https://www.swarmia.com/blog/a-complete-guide-to-code-reviews/",
        # "https://www.swarmia.com/blog/well-researched-advice-on-software-team-productivity/",
        # "https://www.swarmia.com/blog/busting-the-10x-software-engineer-myth/",

        # works but creates too big chunks
        # "https://www.faros.ai/blog/are-you-using-or-about-to-use-dora-metrics-read-this-first",

        # didn't work
        # "https://devinterrupted.com/level-up-your-engineering-management-skills-why-you-should-view-your-mistakes-as-misses",
        # "https://jellyfish.co/blog/engineering-kpis-during-an-economic-downtrun/",
    ]

    loader = UnstructuredURLLoader(urls=urls)

    data = loader.load()

    for url_data in data:
        texts = text_splitter.split_text(url_data.page_content)
        for text in texts:
            chunks.append({"source": url_data.metadata["source"], "content": text})

# PARSE TEXT FILES
elif document_type == "DOCUMENT_TYPE_TXT":
    parsed = []  # used to be a glob, that's why this is pushed to an array
    with open(args.document) as f:
        parsed.append({"source": args.document, "unchunked_content": f.read()})

    for page in parsed:
        texts = text_splitter.split_text(page["unchunked_content"])
        for text in texts:
            chunks.append({"source": page["source"], "content": text})

# LOAD YOUTUBE
elif document_type == "DOCUMENT_TYPE_YOUTUBE":
    from langchain.document_loaders import YoutubeLoader
    loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=JattR1uoX7g", add_video_info=True)
    data = loader.load()
    print(data)
    print("youtube not fully implemented")

# WRITE TO JSON
json_object = json.dumps(chunks)
with open("pg.json", "w") as outfile:
    outfile.write(json_object)

sys.exit()














llm = OpenAI(temperature=0)
conversation = ConversationChain(llm=llm, verbose=True)

print(conversation.predict(input="Hi there!"))
print(conversation.predict(input="I'm doing well! Just having a conversation with an AI."))

sys.exit()

os.environ["SERPAPI_API_KEY"] = ""

# First, let's load the language model we're going to use to control the agent.
llm = OpenAI(temperature=0)

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Now let's test it out!
agent.run("Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?")

sys.exit()

prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

print(prompt.format(product="colorful socks"))

llm = OpenAI(temperature=0.9)
chain = LLMChain(llm=llm, prompt=prompt)

print(chain.run("colorful socks"))

# text = "What would be a good company name for a company that makes colorful socks?"
# print(llm(text))

