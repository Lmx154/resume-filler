from models.schemas import Resume, EnhanceRequest, ContextSettings
from services.ai_service import ai_service

class ResumeService:
    def __init__(self):
        self.context_settings = None

    async def process_resume(self, resume: Resume) -> dict:
        # Process uploaded resume
        return {"status": "success", "content": resume.content}

    async def enhance_resume(self, request: EnhanceRequest) -> str:
        prompt = self._create_enhancement_prompt(request)
        
        if hasattr(ai_service, 'openai_client'):
            return await ai_service.generate_openai_response(prompt, self.context_settings)
        else:
            return await ai_service.generate_ollama_response(prompt)

    def _create_enhancement_prompt(self, request: EnhanceRequest) -> str:
        return f"""
        Job Title: {request.job_title}
        Company: {request.company}
        Field: {request.field}
        
        Original Content:
        {request.resume_content}
        
        Please enhance this content to better match the job requirements while maintaining truthfulness.
        """

    def update_context(self, settings: ContextSettings):
        self.context_settings = settings

resume_service = ResumeService()
