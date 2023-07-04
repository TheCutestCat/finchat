from agents.structure_search import StockPercentageChangeTool,StockPriceTool,StockGetBestPerformingTool
from agents.web_search import GoogleSearchTool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

import gradio as gr
import time

tools = [StockPriceTool(),StockPercentageChangeTool(),StockGetBestPerformingTool(),GoogleSearchTool()]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

test_agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    verbose=True, 
)

def gr_func(info):
    # info = "和30天前相比，谷歌股票价格发生了怎样的变化？"
    # prompt = "for the stock matket price, use the StructuredSearchAgentTool first. for the else question use the GoogleSearchTool, don't mention the tools in the answer"
    ans = test_agent.run(f"{info}")
    return ans


demo = gr.Interface(fn=gr_func, inputs="text", outputs="text")

demo.queue().launch(server_name='0.0.0.0', server_port=7860, share=False, inbrowser=True)