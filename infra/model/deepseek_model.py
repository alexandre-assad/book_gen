from os import getenv
from domain.singleton.singleton import singleton
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

@singleton
class DeepSeekModel:
    def __init__(self) -> None:
        api_key = getenv("DEEPSEEK_API_KEY")

        if not api_key:
            raise ValueError("No API Key")
        
        self.client = OpenAI(api_key=api_key, base_url="") #deepseek api
        self.model_name = "gpt-4o"

    def chat(self, message: str, temperature: float = 0.7) -> str:
        messages = [
        {"role": "user", "content": message}
    ]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
