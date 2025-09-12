from domain.singleton.singleton import singleton
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

load_dotenv()


@singleton
class Gpt4oModel:
    def __init__(self) -> None:
        self._llm = ChatDeepSeek(model="gpt-4o")

    @property
    def llm(self):
        return self._llm
