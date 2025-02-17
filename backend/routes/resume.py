from fastapi import APIRouter, UploadFile, File
from models.schemas import Resume, EnhanceRequest, ContextSettings, AIConfig
from services.resume_service import resume_service
from services.ai_service import ai_service
from services.parser_service import parser_service
from services.system_service import system_service

router = APIRouter(prefix="/api/resume", tags=["resume"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if file.content_type == 'application/pdf' or file.filename.endswith('.pdf'):
            text_content = system_service._read_pdf(content)
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or file.filename.endswith('.docx'):
            text_content = system_service._read_docx(content)
        else:
            text_content = content.decode()
            
        # Parse the resume content
        parsed_data = parser_service.parse_resume(text_content)
        
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
