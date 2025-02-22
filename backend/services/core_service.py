import httpx
from openai import OpenAI
from config import settings
from models.schemas import Resume, EnhanceRequest, ContextSettings
from typing import Dict
from datetime import datetime
import re
import logging

class CoreService:
    def __init__(self):
        self.openai_client = None
        self.ollama_base_url = settings.ollama_base_url
        self.api_base = None
        self.context_settings = None
        self.last_extraction: Dict = {}  # Store last extraction globally
        self.last_resume: Dict = {}  # This will now store both raw and parsed data

    # AI-related methods (from ai_service.py)
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
                json={"model": model, "prompt": prompt}
            )
            return response.json()["response"]

    # Resume-related methods (from resume_service.py)
    async def process_resume(self, resume: Resume) -> dict:
        result = {
            "status": "success",
            "content": resume.content,
            # Initialize parsed data sections that will be updated later
            "parsed_sections": {},
            "metadata": {}
        }
        self.last_resume.clear()
        self.last_resume.update(result)  # Store the last uploaded resume
        return result

    async def enhance_resume(self, request: EnhanceRequest) -> str:
        prompt = self._create_enhancement_prompt(request)
        if self.openai_client:
            return await self.generate_openai_response(prompt, self.context_settings)
        return await self.generate_ollama_response(prompt)

    def _create_enhancement_prompt(self, request: EnhanceRequest) -> str:
        return f"""
        Job Title: {request.job_title}
        Company: {request.company}
        Field: {request.field}
        Original Content: {request.resume_content}
        Please enhance this content to better match the job requirements while maintaining truthfulness.
        """

    def update_context(self, settings: ContextSettings):
        self.context_settings = settings

    # Application-related methods (from application_service.py)
    def process_extracted_text(self, text: str) -> Dict:
        try:
            logging.info(f"Starting extraction with text length: {len(text)}")
            cleaned_text = self._clean_text(text)
            sections = self._split_into_sections(cleaned_text)
            display_text = self._format_for_display(sections)
            metrics = self._calculate_metrics(cleaned_text)

            result = {
                "status": "success",
                "display_text": display_text,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "word_count": metrics["word_count"],
                    "sentence_count": metrics["sentence_count"],
                    "paragraph_count": metrics["paragraph_count"],
                    "estimated_read_time": metrics["estimated_read_time"]
                }
            }
            self.last_extraction.clear()
            self.last_extraction.update(result)
            logging.info(f"Updated last_extraction. Content: {self.last_extraction}")
            return result
        except Exception as e:
            logging.error(f"Error in process_extracted_text: {str(e)}")
            raise

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\r\n]+', '\n', text)
        text = re.sub(r'[^\w\s\n.,!?-]', '', text)
        return text.strip()

    def _split_into_sections(self, text: str) -> list:
        potential_sections = re.split(r'\n(?=[A-Z][^a-z]*:|\d+\.)', text)
        return [s.strip() for s in potential_sections if s.strip()]

    def _format_for_display(self, sections: list) -> str:
        formatted_sections = []
        for i, section in enumerate(sections, 1):
            if ':' in section.split('\n')[0]:
                header, content = section.split(':', 1)
                formatted_sections.append(f"§{i}. {header.strip()}\n{content.strip()}\n")
            else:
                formatted_sections.append(f"§{i}. Section\n{section}\n")
        return "\n".join(formatted_sections)

    def _calculate_metrics(self, text: str) -> Dict:
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "estimated_read_time": len(words) // 200
        }

core_service = CoreService()