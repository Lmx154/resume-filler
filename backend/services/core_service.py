import httpx
from openai import OpenAI, OpenAIError
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
        self.api_base = settings.openai_api_base
        self.context_settings = None
        self.last_extraction: Dict = {}
        self.last_resume: Dict = {}

        try:
            logging.debug(f"Initializing OpenAI with key (first 4 chars): {settings.openai_api_key[:4] if settings.openai_api_key else 'None'}")
            logging.debug(f"Using API base: {settings.openai_api_base}")
            self.init_openai(settings.openai_api_key, settings.openai_api_base)
            logging.info("OpenAI client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise

    def init_openai(self, api_key: str, api_base: str = None):
        self.api_base = api_base or "https://api.openai.com/v1"
        self.openai_client = OpenAI(
            api_key=api_key,
            base_url=self.api_base
        )

    def generate_openai_response(self, prompt: str, context: dict = None) -> str:
        try:
            if not self.openai_client:
                raise Exception("OpenAI client not initialized")
            
            system_content = "You are a professional resume writer."
            if context:
                system_content += "\nAdditional context:"
                system_content += f"\n- Career Level: {context.career_level}"
                system_content += f"\n- Key Skills: {', '.join(context.key_skills)}"
                system_content += f"\n- Preferred Industries: {', '.join(context.preferred_industries)}"
            
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ]
            logging.info(f"Sending request to OpenAI with messages: {messages}")
            
            response = self.openai_client.chat.completions.create(
                model="gpt-35-turbo-16k",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            logging.info(f"Raw OpenAI response: {response}")
            if not response or not hasattr(response, 'choices') or not response.choices:
                raise Exception(f"Invalid response from OpenAI: {response}")
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            logging.error(f"OpenAI API specific error: {str(e)}")
            raise Exception(f"OpenAI API failure: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error in OpenAI call: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")

    def generate_ollama_response(self, prompt: str, model: str = "llama2") -> str:
        with httpx.Client() as client:
            response = client.post(
                f"{self.ollama_base_url}/api/generate",
                json={"model": model, "prompt": prompt}
            )
            return response.json()["response"]

    def process_resume(self, resume: Resume) -> dict:
        result = {
            "status": "success",
            "content": resume.content,
            "parsed_sections": {},
            "metadata": {}
        }
        self.last_resume.clear()
        self.last_resume.update(result)
        return result

    def enhance_resume(self, request: EnhanceRequest) -> str:
        prompt = self._create_enhancement_prompt(request)
        if self.openai_client:
            return self.generate_openai_response(prompt, self.context_settings)
        return self.generate_ollama_response(prompt)

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