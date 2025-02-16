import httpx
from openai import OpenAI
from config import settings
import logging

class AIService:
    def __init__(self):
        self.openai_client = None
        self.ollama_url = settings.ollama_base_url
        self.api_base = None

    def init_openai(self, api_key: str, api_base: str = None):
        self.api_base = api_base
        self.openai_client = OpenAI(
            api_key=api_key,
            base_url=api_base if api_base else "https://api.openai.com/v1"
        )

    async def generate_openai_response(self, prompt: str, context: dict) -> str:
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            raise

    async def generate_ollama_response(self, prompt: str, model: str = "llama2") -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt
                }
            )
            return response.json()["response"]

ai_service = AIService()
