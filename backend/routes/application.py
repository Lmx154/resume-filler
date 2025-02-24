from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.core_service import core_service
import logging

router = APIRouter(prefix="/api/application", tags=["application"])

class ExtractRequest(BaseModel):
    text: str

class EnhanceApplicationRequest(BaseModel):
    enhancement_focus: str
    resume_content: str
    application_content: str  # Now accepts DOM content
    industry_focus: str
    target_keywords: str
    company_culture: str
    additional_info: Optional[dict] = None

@router.post("/extract")
def extract_application(request: ExtractRequest):
    try:
        logging.info("Received extraction request")
        result = core_service.process_extracted_text(request.text)
        logging.info(f"Result: {result['status']}")
        return result
    except Exception as e:
        logging.error(f"Error in extract_application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enhance")
def enhance_application(request: EnhanceApplicationRequest):
    try:
        logging.info("Received enhancement request")
        additional_info_str = ""
        if request.additional_info and isinstance(request.additional_info, dict):
            additional_info_str = "\nAdditional Information: " + ", ".join(f"{k}: {v}" for k, v in request.additional_info.items())

        # Step 1: Use AI to identify fields and suggest auto-fill values from DOM
        prompt = f"""
        Resume Content:
        {request.resume_content}

        Scraped Job Application Form DOM Content:
        {request.application_content}

        Enhancement Focus: {request.enhancement_focus}
        Industry Focus: {request.industry_focus}
        Target Keywords: {request.target_keywords}
        Company Culture Notes: {request.company_culture}
        {additional_info_str}

        Analyze the DOM content of the job application form to identify all fields requiring auto-completion (e.g., personal information, education, skills, experience, additional questions, etc.).
        Look for input fields, textareas, and placeholders to determine field names (e.g., use 'placeholder' attributes like 'Enter your full name' to infer 'Full Name').
        Using the resume content and any additional information provided, generate responses to auto-complete these fields, ensuring the responses are derived from the resume, align with the enhancement focus, incorporate target keywords, reflect the company culture, include any additional information, and are professional, concise, and truthful.
        Suggest a likely DOM selector for each field, prioritizing 'input[placeholder*="..."]', 'textarea[placeholder*="..."]', 'input[name="..."]', or 'textarea[name="..."]' based on the DOM structure. Ensure selectors are specific and match the field’s purpose (e.g., 'input[placeholder="Enter your full name"]' for 'Full Name').
        Return only the field names, their corresponding values, and optional selectors in plain text format, one per line, like this: 'Field: Value [Selector]'. If no selector is available, omit the '[Selector]' part. Do not include any additional text, formatting (e.g., Markdown), or explanations.
        """
        enhanced_content = core_service.generate_openai_response(prompt)

        # Step 2: Return the enhanced content for auto-filling
        return {"status": "success", "enhanced_content": enhanced_content}
    except Exception as e:
        logging.error(f"Error in enhance_application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/last_extract")
def get_last_extraction():
    last_extraction = core_service.last_extraction
    logging.info(f"Getting last extraction. Full content: {last_extraction}")
    if not last_extraction:
        logging.warning("No extraction data available")
        return {"status": "pending", "message": "No extraction data available"}
    if 'status' not in last_extraction or 'display_text' not in last_extraction:
        logging.error(f"Invalid last_extraction structure: {last_extraction.keys()}")
        return {"status": "error", "message": "Invalid data structure"}
    logging.info(f"Returning extraction with text length: {len(last_extraction.get('display_text', ''))}")
    return last_extraction