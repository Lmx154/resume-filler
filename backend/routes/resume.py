from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from models.schemas import Resume, EnhanceRequest, AIConfig
from services.core_service import core_service
from services.file_service import file_service
import io
from typing import Optional, Dict

router = APIRouter(prefix="/api/resume", tags=["resume"])

class ResumeUploadRequest(BaseModel):
    enhancement_focus: str
    industry_focus: str
    target_keywords: str
    company_culture: str
    additional_info: Optional[Dict[str, str]] = None

@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    enhancement_focus: str = Form(default="Clarity & Conciseness"),
    industry_focus: str = Form(default="Technology"),
    target_keywords: str = Form(default=""),
    company_culture: str = Form(default=""),
    additional_info: str = Form(default="{}")  # JSON string for additional_info
):
    try:
        content = file.file.read()
        if file.content_type == 'application/pdf' or file.filename.endswith('.pdf'):
            text_content = file_service._read_pdf_from_bytes(io.BytesIO(content))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or file.filename.endswith('.docx'):
            text_content = file_service._read_docx_from_bytes(io.BytesIO(content))
        else:
            text_content = content.decode()
        parsed_data = file_service.parse_resume(text_content)

        # Parse additional_info from JSON string
        additional_info_dict = {}
        try:
            if additional_info:
                additional_info_dict = json.loads(additional_info) if additional_info.strip() else {}
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format for additional_info")

        core_service.process_resume(
            Resume(
                content=text_content,
                file_name=file.filename,
                file_type=file.content_type
            ),
            enhancement_focus=enhancement_focus,
            industry_focus=industry_focus,
            target_keywords=target_keywords,
            company_culture=company_culture,
            additional_info=additional_info_dict
        )
        core_service.last_resume.update({
            "parsed_sections": parsed_data["parsed_sections"],
            "metadata": parsed_data["metadata"],
            "enhancement_focus": enhancement_focus,
            "industry_focus": industry_focus,
            "target_keywords": target_keywords,
            "company_culture": company_culture,
            "additional_info": additional_info_dict
        })
        return {
            "status": "success",
            "parsed_sections": parsed_data["parsed_sections"],
            "summary": parsed_data["summary"],
            "metadata": parsed_data["metadata"],
            "settings": {
                "enhancement_focus": enhancement_focus,
                "industry_focus": industry_focus,
                "target_keywords": target_keywords,
                "company_culture": company_culture,
                "additional_info": additional_info_dict
            }
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
        "metadata": last_resume["metadata"],
        "settings": {
            "enhancement_focus": last_resume.get("enhancement_focus", "Clarity & Conciseness"),
            "industry_focus": last_resume.get("industry_focus", "Technology"),
            "target_keywords": last_resume.get("target_keywords", ""),
            "company_culture": last_resume.get("company_culture", ""),
            "additional_info": last_resume.get("additional_info", {})
        }
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
        core_service.process_resume(
            Resume(
                content=text_content,
                file_name=request.file_path,
                file_type=request.file_path.split('.')[-1]
            )
        )
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

import json  # Add this import at the top of the file