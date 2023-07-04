from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent
from dotenv import load_dotenv
import os
load_dotenv()

search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

memory = ConversationBufferMemory(memory_key="chat_history")
llm=OpenAI(temperature=0)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

agent_tool = [
    Tool(
        name = "Current Search",
        func=agent_chain.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]
agent_tool_chain = initialize_agent(agent_tool, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

ans = agent_tool_chain.run(input="the temperature in beijing")
print("###################",ans)