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
    application_content: str
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
            additional_info_str = "\nAdditional Information:\n" + "\n".join(f"- {k}: {v}" for k, v in request.additional_info.items())

        prompt = f"""
        You are a professional resume writer tasked with auto-filling a job application form based on a user's resume. Below is the information provided:

        Resume Content:
        {request.resume_content}

        Scraped Job Application Form DOM Content:
        {request.application_content}

        Enhancement Focus: {request.enhancement_focus}
        Industry Focus: {request.industry_focus}
        Target Keywords: {request.target_keywords}
        Company Culture Notes: {request.company_culture}
        {additional_info_str}

        Instructions:
        1. Analyze the DOM content to identify all fields requiring auto-completion (e.g., personal information, education, skills, experience, additional questions).
        2. Use 'placeholder' attributes (e.g., 'Enter your full name') or 'name' attributes to infer field purposes.
        3. Generate truthful responses derived from the resume content, tailored to the enhancement focus:
           - For "Clarity & Conciseness": Provide short, clear answers.
           - For "Professional Tone": Use formal language and structure.
           - For "Keywords Optimization": Incorporate the target keywords naturally.
           - For "Impact & Achievement Focus": Highlight results and accomplishments.
        4. Align responses with the industry focus and reflect the company culture notes where relevant.
        5. Incorporate any additional information provided to enhance specific fields.
        6. Suggest a DOM selector for each field (e.g., 'input[placeholder="Enter your full name"]', 'textarea[name="experience"]') based on the DOM structure. If no clear selector is identifiable, omit it.
        7. Return the results in plain text format, one field per line, as 'Field: Value [Selector]' (omit [Selector] if not applicable). Do not include extra explanations or formatting.
        """
        enhanced_content = core_service.generate_openai_response(prompt)
        
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