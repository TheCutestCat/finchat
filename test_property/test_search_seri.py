from dotenv import load_dotenv
import os
load_dotenv()
from langchain.utilities import GoogleSerperAPIWrapper

search = GoogleSerperAPIWrapper()
ans = search.run("What stock evaluators are saying about Nvidia")
print(ans)
print(len(ans))