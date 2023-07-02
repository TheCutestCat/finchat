from langchain import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper


# Initialize the OpenAI language model
#Replace <your_api_key> in openai_api_key="<your_api_key>" with your actual OpenAI key.
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# Initialize the SerpAPIWrapper for search functionality
#Replace <your_api_key> in openai_api_key="<your_api_key>" with your actual SerpAPI key.

search = GoogleSerperAPIWrapper
# Define a list of tools offered by the agent
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful when you need to answer questions about current events. You should ask targeted questions."
    ),
]


mrkl = initialize_agent(tools, llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True)

# Do this so we can see exactly what's going on under the hood
import langchain
langchain.debug = False

mrkl.run(
    "What is the weather in LA and SF?"
)