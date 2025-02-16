from pydantic import BaseModel
from typing import Optional, List

class Resume(BaseModel):
    content: str
    file_name: str
    file_type: str

class EnhanceRequest(BaseModel):
    job_title: str
    company: str
    field: str
    resume_content: str

class ContextSettings(BaseModel):
    career_level: str
    key_skills: List[str]
    preferred_industries: List[str]

class AIConfig(BaseModel):
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class EnhanceResponse(BaseModel):
    enhanced_content: str
    original_content: str
