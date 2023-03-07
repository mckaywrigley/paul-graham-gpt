import os
import sys
import glob
import json
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import NLTKTextSplitter

from dotenv import load_dotenv

load_dotenv()

import pprint
pp = pprint.PrettyPrinter(indent=4)

# CHUNKS TO PUT IN JSON
chunks = []

text_splitter = NLTKTextSplitter(chunk_size=1000)

# SPLIT PDFS
"""
from langchain.document_loaders import PagedPDFSplitter

loader = PagedPDFSplitter("sources/2022_state_of_devops_report.pdf")
pages = loader.load_and_split()


for page in pages:
    texts = text_splitter.split_text(page.page_content)
    for text in texts:
        chunks.append(
            {"source": "sources/2022_state_of_devops_report.pdf", "content": text}
        )
"""

# SCRAPE FROM URL
"""
urls = [
    # works
    "https://www.swarmia.com/blog/developer-experience-what-why-how/",
    "https://www.swarmia.com/blog/size-age-culture-productivity/",
    "https://www.swarmia.com/blog/continuous-improvement-in-software-development/",
    "https://www.swarmia.com/blog/daily-stand-ups/",
    "https://www.swarmia.com/blog/velocity-vs-cycle-time/",
    "https://www.swarmia.com/blog/space-framework/",
    "https://www.swarmia.com/blog/dora-change-failure-rate/",
    "https://www.swarmia.com/blog/balancing-engineering-investments/",
    "https://www.swarmia.com/blog/ship-software-10x-faster/",
    "https://www.swarmia.com/blog/product-development-performance-for-investors/",
    "https://www.swarmia.com/blog/dora-metrics/",
    "https://www.swarmia.com/blog/software-engineers-learn-on-company-time/",
    "https://www.swarmia.com/blog/issue-cycle-time/",
    "https://www.swarmia.com/blog/agile-team-working-agreements/",
    "https://www.swarmia.com/blog/measuring-software-development-productivity/",
    "https://www.swarmia.com/blog/data-driven-retrospectives-stop-fake-improvements/",
    "https://www.swarmia.com/blog/a-complete-guide-to-code-reviews/",
    "https://www.swarmia.com/blog/well-researched-advice-on-software-team-productivity/",
    "https://www.swarmia.com/blog/busting-the-10x-software-engineer-myth/",

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
"""

# PARSE TEXT FILES
parsed = []
for txt_file in glob.glob("sources/*.txt"):
    with open(txt_file) as f:
        parsed.append({"source": txt_file, "unchunked_content": f.read()})

for page in parsed:
    texts = text_splitter.split_text(page["unchunked_content"])
    for text in texts:
        chunks.append({"source": page["source"], "content": text})

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

