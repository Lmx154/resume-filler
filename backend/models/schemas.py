from pydantic import BaseModel
from typing import Optional, Dict

class Resume(BaseModel):
    content: str
    file_name: str
    file_type: str
    enhancement_focus: Optional[str] = "Clarity & Conciseness"
    industry_focus: Optional[str] = "Technology"
    target_keywords: Optional[str] = ""
    company_culture: Optional[str] = ""
    additional_info: Optional[Dict[str, str]] = None

class EnhanceRequest(BaseModel):
    job_title: str
    company: str
    field: str
    resume_content: str

class AIConfig(BaseModel):
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    model: Optional[str] = "gpt-4o-mini"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class EnhanceResponse(BaseModel):
    enhanced_content: str
    original_content: str