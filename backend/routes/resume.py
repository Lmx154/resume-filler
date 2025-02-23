from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from models.schemas import Resume, EnhanceRequest, AIConfig
from services.core_service import core_service
from services.file_service import file_service
import io

router = APIRouter(prefix="/api/resume", tags=["resume"])

@router.post("/upload")
def upload_resume(file: UploadFile = File(...)):
    try:
        content = file.file.read()
        if file.content_type == 'application/pdf' or file.filename.endswith('.pdf'):
            text_content = file_service._read_pdf_from_bytes(io.BytesIO(content))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or file.filename.endswith('.docx'):
            text_content = file_service._read_docx_from_bytes(io.BytesIO(content))
        else:
            text_content = content.decode()
        parsed_data = file_service.parse_resume(text_content)

        core_service.process_resume(Resume(
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
def get_last_uploaded_resume():
    last_resume = core_service.last_resume
    if not last_resume or "parsed_sections" not in last_resume:
        return {"status": "pending", "message": "No resume uploaded yet"}
    return {
        "status": "success",
        "parsed_sections": last_resume["parsed_sections"],
        "metadata": last_resume["metadata"]
    }

@router.get("/last_upload")
def get_last_upload():
    last_resume = core_service.last_resume
    if not last_resume:
        return {"status": "pending", "message": "No resume uploaded yet"}
    return last_resume

@router.post("/enhance")
def enhance_resume(request: EnhanceRequest):
    return core_service.enhance_resume(request)

@router.post("/ai-config")
def update_ai_config(config: AIConfig):
    if config.api_key:
        core_service.init_openai(config.api_key, config.endpoint)
    return {"status": "success"}

class FilePathRequest(BaseModel):
    file_path: str

@router.post("/read-from-path")
def read_resume_from_path(request: FilePathRequest):
    try:
        text_content = file_service.read_file_content(request.file_path)
        parsed_data = file_service.parse_resume(text_content)
        core_service.process_resume(Resume(
            content=text_content,
            file_name=request.file_path,
            file_type=request.file_path.split('.')[-1]
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