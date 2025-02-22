from fastapi import APIRouter, UploadFile, File
from models.schemas import Resume, EnhanceRequest, ContextSettings, AIConfig
from services.core_service import core_service
from services.file_service import file_service
import io

router = APIRouter(prefix="/api/resume", tags=["resume"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if file.content_type == 'application/pdf' or file.filename.endswith('.pdf'):
            # Wrap bytes in a BytesIO object for PyPDF2
            text_content = file_service._read_pdf(io.BytesIO(content))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or file.filename.endswith('.docx'):
            # Wrap bytes in a BytesIO object for python-docx
            text_content = file_service._read_docx(io.BytesIO(content))
        else:
            text_content = content.decode()
        parsed_data = file_service.parse_resume(text_content)
        
        # Store both raw content and parsed data
        await core_service.process_resume(Resume(
            content=text_content,
            file_name=file.filename,
            file_type=file.content_type
        ))
        core_service.last_resume.update({
            "parsed_sections": parsed_data["parsed_sections"],
            "metadata": parsed_data["metadata"]
        })
        
        return {
            "status": "success",
            "parsed_sections": parsed_data["parsed_sections"],
            "summary": parsed_data["summary"],
            "metadata": parsed_data["metadata"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/upload")
async def get_last_uploaded_resume():
    last_resume = core_service.last_resume
    if not last_resume or "parsed_sections" not in last_resume:
        return {"status": "pending", "message": "No resume uploaded yet"}
    return {
        "status": "success",
        "parsed_sections": last_resume["parsed_sections"],
        "metadata": last_resume["metadata"]
    }

@router.get("/last_upload")
async def get_last_upload():
    last_resume = core_service.last_resume
    if not last_resume:
        return {"status": "pending", "message": "No resume uploaded yet"}
    return last_resume

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