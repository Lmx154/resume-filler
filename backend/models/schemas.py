from pydantic import BaseModel
from typing import Optional

class Resume(BaseModel):
    content: str
    file_name: str
    file_type: str

class EnhanceRequest(BaseModel):
    job_title: str
    company: str
    field: str
    resume_content: str

class AIConfig(BaseModel):
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class EnhanceResponse(BaseModel):
    enhanced_content: str
    original_content: str

class EnhanceApplicationRequest(BaseModel):
    enhancement_focus: str
    resume_content: str
    application_content: str
    industry_focus: str
    target_keywords: str
    company_culture: str