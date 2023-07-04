from agents.structure_search import structured_search_agent,StructuredSearchAgentTool
from agents.web_search import web_search,GoogleSearchTool
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

tools = [StructuredSearchAgentTool(),GoogleSearchTool()]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

test_agent = initialize_agent(tools,
                        llm,
                        agent=AgentType.OPENAI_FUNCTIONS,
                        verbose=True)

info = "谷歌的总部在哪里？"
print('-'*8 + f"{info}"+ '-'*8 )
print(test_agent.run(f"{info}"))
print()