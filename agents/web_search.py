from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
load_dotenv()

def google_search(question):
    #search info is limited, we oly use a very little information for this.
    search = GoogleSerperAPIWrapper()
    ans = search.run("question")
    # lenth cutoff
    max_length = 3000
    if len(ans) > max_length:
        ans = ans[:max_length]
    return ans

class GoogleSearchCheckInput(BaseModel):
    """Input for google search check."""

    question: str = Field(..., description="the quesntion for the google search")
    
class GoogleSearchTool(BaseTool):
    name = "google_search"
    description = "Useful for when you need to find out information for some companies,You should input the quesntion used on the google search API."

    def _run(self, question: str):
        ans = google_search(question)

        return ans

    def _arun(self, question: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GoogleSearchCheckInput
    
    
tools = [GoogleSearchTool()]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

web_search = initialize_agent(tools,
                        llm,
                        agent=AgentType.OPENAI_FUNCTIONS,
                        verbose=False)


if __name__ == "__main__":
    
    info = "根据过去一年的表现，我应该尝试去投资美国国债，还是应该去投资纳斯达克股票"
    print('-'*8 + f"{info}"+ '-'*8 )
    print(web_search.run(f"{info}"))
    print()
    
    info = "谷歌的总部的位置在哪里？"
    print('-'*8 + f"{info}"+ '-'*8 )
    print(web_search.run(f"{info}"))
    print()
    
    info = "谷歌有多少员工？"
    print('-'*8 + f"{info}"+ '-'*8 )
    print(web_search.run(f"{info}"))
    print()
    
    info = "投资人对谷歌的评价是怎样的？"
    print('-'*8 + f"{info}"+ '-'*8 )
    print(web_search.run(f"{info}"))
    print()
    
    info = "谷歌的创始人是谁？"
    print('-'*8 + f"{info}"+ '-'*8 )
    print(web_search.run(f"{info}"))
    print()