import os
import sys
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.document_loaders import UnstructuredURLLoader

from dotenv import load_dotenv

load_dotenv()

import pprint
pp = pprint.PrettyPrinter(indent=4)

from langchain.document_loaders import PagedPDFSplitter

loader = PagedPDFSplitter("sources/2022_state_of_devops_report.pdf")
pages = loader.load_and_split()

from langchain.text_splitter import NLTKTextSplitter
text_splitter = NLTKTextSplitter(chunk_size=1000)

for page in pages:
    texts = text_splitter.split_text(page.page_content)
    print(texts)


sys.exit()

urls = [
    # works
    "https://www.swarmia.com/blog/developer-experience-what-why-how/",
    # didn't work
    # "https://devinterrupted.com/level-up-your-engineering-management-skills-why-you-should-view-your-mistakes-as-misses",
    # "https://jellyfish.co/blog/engineering-kpis-during-an-economic-downtrun/",
]

loader = UnstructuredURLLoader(urls=urls)

data = loader.load()

print(data)

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

