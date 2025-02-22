from fastapi import APIRouter, UploadFile, File
from models.schemas import Resume, EnhanceRequest, ContextSettings, AIConfig
from services.core_service import core_service
from services.file_service import file_service

router = APIRouter(prefix="/api/resume", tags=["resume"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if file.content_type == 'application/pdf' or file.filename.endswith('.pdf'):
            text_content = file_service._read_pdf(content)
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or file.filename.endswith('.docx'):
            text_content = file_service._read_docx(content)
        else:
            text_content = content.decode()
        parsed_data = file_service.parse_resume(text_content)
        return {
            "status": "success",
            "parsed_sections": parsed_data["parsed_sections"],
            "summary": parsed_data["summary"],
            "metadata": parsed_data["metadata"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/enhance")
async def enhance_resume(request: EnhanceRequest):
    return await core_service.enhance_resume(request)

@router.post("/context")
async def update_context(settings: ContextSettings):
    core_service.update_context(settings)
    return {"status": "success"}

@router.post("/ai-config")
async def update_ai_config(config: AIConfig):
    if config.api_key:
        core_service.init_openai(config.api_key, config.endpoint)
    return {"status": "success"}