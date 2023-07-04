
from langchain.utilities import WikipediaAPIWrapper

wikipedia = WikipediaAPIWrapper()

ans = wikipedia.run("nvidia")
print('$'*10)
print(ans)
print(len(ans))