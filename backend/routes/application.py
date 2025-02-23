from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.core_service import core_service  # Correct import
import logging

router = APIRouter(prefix="/api/application", tags=["application"])

class ExtractRequest(BaseModel):
    text: str

class EnhanceApplicationRequest(BaseModel):
    application_type: str
    company: str
    enhancement_focus: str
    resume_content: str
    application_content: str

@router.post("/extract")
def extract_application(request: ExtractRequest):
    try:
        logging.info("Received extraction request")
        result = core_service.process_extracted_text(request.text)  # Use core_service instance
        logging.info(f"Result: {result['status']}")
        
        # No need for global check since core_service manages last_extraction internally
        return result
    except Exception as e:
        logging.error(f"Error in extract_application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enhance")
def enhance_application(request: EnhanceApplicationRequest):
    try:
        logging.info("Received enhancement request")
        prompt = f"""
        Resume Content:
        {request.resume_content}

        Job Application Form Content:
        {request.application_content}

        Application Type: {request.application_type}
        Company: {request.company}
        Enhancement Focus: {request.enhancement_focus}

        Based on the resume and job application form content provided, generate a tailored response for the application form fields.
        Ensure the response aligns with the enhancement focus and is professional, concise, and truthful.
        """
        enhanced_content = core_service.generate_openai_response(prompt, core_service.context_settings)
        return {
            "status": "success",
            "enhanced_content": enhanced_content
        }
    except Exception as e:
        logging.error(f"Error in enhance_application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/last_extract")
def get_last_extraction():
    last_extraction = core_service.last_extraction  # Access via instance
    logging.info(f"Getting last extraction. Full content: {last_extraction}")
    
    if not last_extraction:
        logging.warning("No extraction data available")
        return {"status": "pending", "message": "No extraction data available"}
        
    if 'status' not in last_extraction or 'display_text' not in last_extraction:
        logging.error(f"Invalid last_extraction structure: {last_extraction.keys()}")
        return {"status": "error", "message": "Invalid data structure"}
    
    logging.info(f"Returning extraction with text length: {len(last_extraction.get('display_text', ''))}")
    return last_extraction