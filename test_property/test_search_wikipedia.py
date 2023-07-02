
from langchain.utilities import WikipediaAPIWrapper

wikipedia = WikipediaAPIWrapper()

ans = wikipedia.run("tesla")
print(ans)