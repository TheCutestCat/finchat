from dotenv import load_dotenv
import os
load_dotenv()
from langchain.utilities import GoogleSerperAPIWrapper

search = GoogleSerperAPIWrapper()
ans = search.run("英伟达最近的新闻?")
print(ans)