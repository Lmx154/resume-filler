from fastapi import APIRouter, UploadFile, File
from models.schemas import Resume, EnhanceRequest, ContextSettings, AIConfig
from services.resume_service import resume_service
from services.ai_service import ai_service

router = APIRouter(prefix="/api/resume", tags=["resume"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    resume = Resume(
        content=content.decode(),
        file_name=file.filename,
        file_type=file.content_type
    )
    return await resume_service.process_resume(resume)

@router.post("/enhance")
async def enhance_resume(request: EnhanceRequest):
    return await resume_service.enhance_resume(request)

@router.post("/context")
async def update_context(settings: ContextSettings):
    resume_service.update_context(settings)
    return {"status": "success"}

@router.post("/ai-config")
async def update_ai_config(config: AIConfig):
    if config.api_key:
        ai_service.init_openai(config.api_key)
    return {"status": "success"}
