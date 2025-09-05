from os import getenv
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class DeepSeekModel:
    def __init__(self, model_name: str = "gpt-4o"):
        # api_key = getenv("DEEPSEEK_API_KEY")
        api_key = getenv("GPT_API_KEY")

        if not api_key:
            raise ValueError("No API Key")
        
        self.client = OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")
        self.model_name = model_name

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

