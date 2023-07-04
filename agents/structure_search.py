import yfinance as yf

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return round(todays_data['Close'][0], 2)


from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI


from pydantic import BaseModel, Field

class StockPriceCheckInput(BaseModel):
    """Input for Stock price check."""

    stockticker: str = Field(..., description="Ticker symbol for stock or index")
    
class StockPriceTool(BaseTool):
    name = "get_stock_ticker_price"
    description = "Useful for when you need to find out the price of stock. You should input the stock ticker used on the yfinance API"

    def _run(self, stockticker: str):
        # print("i'm running")
        price_response = get_stock_price(stockticker)

        return price_response

    def _arun(self, stockticker: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput
    

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage
model = ChatOpenAI(model="gpt-3.5-turbo-0613")
from langchain.tools import MoveFileTool, format_tool_to_openai_function

from datetime import datetime, timedelta

def get_price_change_percent(symbol, days_ago):
    ticker = yf.Ticker(symbol)

    # Get today's date
    end_date = datetime.now()

    # Get the date N days ago
    start_date = end_date - timedelta(days=days_ago)

    # Convert dates to string format that yfinance can accept
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    # Get the historical data
    historical_data = ticker.history(start=start_date, end=end_date)

    # Get the closing price N days ago and today's closing price
    old_price = historical_data['Close'].iloc[0]
    new_price = historical_data['Close'].iloc[-1]

    # Calculate the percentage change
    percent_change = ((new_price - old_price) / old_price) * 100

    return round(percent_change, 2)

def calculate_performance(symbol, days_ago):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    historical_data = ticker.history(start=start_date, end=end_date)
    old_price = historical_data['Close'].iloc[0]
    new_price = historical_data['Close'].iloc[-1]
    percent_change = ((new_price - old_price) / old_price) * 100
    return round(percent_change, 2)

def get_best_performing(stocks, days_ago):
    best_stock = None
    best_performance = None
    for stock in stocks:
        try:
            performance = calculate_performance(stock, days_ago)
            if best_performance is None or performance > best_performance:
                best_stock = stock
                best_performance = performance
        except Exception as e:
            print(f"Could not calculate performance for {stock}: {e}")
    return best_stock, best_performance

from typing import List

class StockChangePercentageCheckInput(BaseModel):
    """Input for Stock ticker check. for percentage check"""

    stockticker: str = Field(..., description="Ticker symbol for stock or index")
    days_ago: int = Field(..., description="Int number of days to look back")

class StockPercentageChangeTool(BaseTool):
    name = "get_price_change_percent"
    description = "Useful for when you need to find out the percentage change in a stock's value. You should input the stock ticker used on the yfinance API and also input the number of days to check the change over"

    def _run(self, stockticker: str, days_ago: int):
        price_change_response = get_price_change_percent(stockticker, days_ago)

        return price_change_response

    def _arun(self, stockticker: str, days_ago: int):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockChangePercentageCheckInput


# the best performing

class StockBestPerformingInput(BaseModel):
    """Input for Stock ticker check. for percentage check"""

    stocktickers: List[str] = Field(..., description="Ticker symbols for stocks or indices")
    days_ago: int = Field(..., description="Int number of days to look back")

class StockGetBestPerformingTool(BaseTool):
    name = "get_best_performing"
    description = "Useful for when you need to the performance of multiple stocks over a period. You should input a list of stock tickers used on the yfinance API and also input the number of days to check the change over"

    def _run(self, stocktickers: List[str], days_ago: int):
        price_change_response = get_best_performing(stocktickers, days_ago)

        return price_change_response

    def _arun(self, stockticker: List[str], days_ago: int):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StockBestPerformingInput





tools = [StockPriceTool(),StockPercentageChangeTool(),StockGetBestPerformingTool()]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

structured_search_agent = initialize_agent(tools,
                        llm,
                        agent=AgentType.OPENAI_FUNCTIONS,
                        verbose=True)



class StructuredSearchAgentCheckInput(BaseModel):
    """Input for Stock price check."""

    question: str = Field(..., description="question on the stock price")
    
class StructuredSearchAgentTool(BaseTool):
    name = "structured_search_agent"
    description = "Useful for when you need to calculate stock price of a company. You should input qusention on stock price of a company"

    def _run(self, question: str):
        # print("i'm running")
        price_response = structured_search_agent.run(question)

        return price_response

    def _arun(self, question: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = StructuredSearchAgentCheckInput




if __name__ == "__main__":
    
    # info = "谷歌股票的当前价格是多少？"
    # print('-'*8 + f"{info}"+ '-'*8 )
    # print(structured_search_agent.run(f"{info}"))
    # print()
    
    info = "谷歌股票的价格是多少？和一年前作比较，股票价格是涨还是跌？"
    print('-'*8 + f"{info}"+ '-'*8 )
    print(structured_search_agent.run(f"{info}"))
    print()
    
    # info = "苹果股票和谷歌的股票这两者过去三十天哪个上涨幅度更大？"
    # print('-'*8 + f"{info}"+ '-'*8 )
    # print(structured_search_agent.run(f"{info}"))
    # print()
    
    # info = "苹果 谷歌 亚马逊这三者过去三十天表现最好的是哪一个？"
    # print('-'*8 + f"{info}"+ '-'*8 )
    # print(structured_search_agent.run(f"{info}"))
    # print()