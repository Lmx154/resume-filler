import httpx
from openai import OpenAI, OpenAIError
from config import settings
from models.schemas import Resume, EnhanceRequest
from typing import Dict, Optional
from datetime import datetime
import re
import logging

class CoreService:
    def __init__(self):
        self.openai_client = None
        self.ollama_base_url = settings.ollama_base_url
        self.api_base = settings.openai_api_base
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

    def generate_openai_response(self, prompt: str) -> str:
        try:
            if not self.openai_client:
                raise Exception("OpenAI client not initialized")
            
            model = settings.model
            messages = [
                {"role": "system", "content": "You are a professional resume writer."},
                {"role": "user", "content": prompt}
            ]
            logging.info(f"Sending request to OpenAI with model: {model}, messages: {messages}")
            
            response = self.openai_client.chat.completions.create(
                model=model,
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
            response = client.post(f"{self.ollama_base_url}/api/generate", json={"model": model, "prompt": prompt})
            return response.json()["response"]

    def process_resume(self, resume: Resume) -> dict:
        result = {
            "status": "success",
            "content": resume.content,
            "parsed_sections": {},
            "metadata": {},
            "enhancement_focus": resume.enhancement_focus,
            "industry_focus": resume.industry_focus,
            "target_keywords": resume.target_keywords,
            "company_culture": resume.company_culture,
            "additional_info": resume.additional_info or {}
        }
        self.last_resume.clear()
        self.last_resume.update(result)
        return result

    def enhance_resume(self, request: EnhanceRequest) -> str:
        prompt = self._create_enhancement_prompt(request)
        return self.generate_openai_response(prompt) if self.openai_client else self.generate_ollama_response(prompt)

    def _create_enhancement_prompt(self, request: EnhanceRequest) -> str:
        # Use stored resume settings for enhancement
        last_resume = self.last_resume
        if not last_resume or "content" not in last_resume:
            raise Exception("No resume uploaded yet")
        
        additional_info_str = ""
        if last_resume.get("additional_info", {}) and isinstance(last_resume["additional_info"], dict):
            additional_info_str = "\nAdditional Information:\n" + "\n".join(f"- {k}: {v}" for k, v in last_resume["additional_info"].items())

        prompt = f"""
        You are a professional resume writer tasked with auto-filling a job application form based on a user's resume. Below is the information provided:

        Resume Content:
        {last_resume["content"]}

        Job Application Context:
        Job Title: {request.job_title}
        Company: {request.company}
        Field: {request.field}

        Enhancement Focus: {last_resume.get("enhancement_focus", "Clarity & Conciseness")}
        Industry Focus: {last_resume.get("industry_focus", "Technology")}
        Target Keywords: {last_resume.get("target_keywords", "")}
        Company Culture Notes: {last_resume.get("company_culture", "")}
        {additional_info_str}

        Instructions:
        1. Analyze the job application context to identify fields requiring auto-completion (e.g., personal information, education, skills, experience, additional questions).
        2. Use the resume content to generate truthful responses, tailored to the enhancement focus:
           - For "Clarity & Conciseness": Provide short, clear answers.
           - For "Professional Tone": Use formal language and structure.
           - For "Keywords Optimization": Incorporate the target keywords naturally.
           - For "Impact & Achievement Focus": Highlight results and accomplishments.
        3. Align responses with the industry focus and reflect the company culture notes where relevant.
        4. Incorporate any additional information provided to enhance specific fields, such as 'Current GPA' if provided in Additional Information.
        5. Return the results in plain text format, one field per line, as 'Field: Value'. Do not include selectors or extra explanations or formatting.
        """
        return prompt

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
        return re.sub(r'[\s\n.,!?-]+', ' ', text).strip()

    def _split_into_sections(self, text: str) -> list:
        return [s.strip() for s in re.split(r'\n(?=[A-Z][^a-z]*:|\d+\.)', text) if s.strip()]

    def _format_for_display(self, sections: list) -> str:
        return "\n".join(f"§{i}. {s.split(':', 1)[0].strip()}\n{s.split(':', 1)[1].strip()}\n" if ':' in s.split('\n')[0] else f"§{i}. Section\n{s}\n" for i, s in enumerate(sections, 1))

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