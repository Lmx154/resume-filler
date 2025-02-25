from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.core_service import core_service
import logging

router = APIRouter(prefix="/api/application", tags=["application"])

class EnhanceApplicationRequest(BaseModel):
    enhancement_focus: str
    resume_content: str
    application_content: str
    industry_focus: str
    target_keywords: str
    company_culture: str
    additional_info: Optional[dict] = None

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
        5. Incorporate any additional information provided to enhance specific fields, such as 'Current GPA' if provided in Additional Information.
        6. Suggest a DOM selector for each field (e.g., 'input[placeholder="Enter your full name"]', 'textarea[name="experience"]') based on the DOM structure. If no clear selector is identifiable, omit it.
        7. Return the results in plain text format, one field per line, as 'Field: Value [Selector]' (omit [Selector] if not applicable). Do not include extra explanations or formatting.
        """
        enhanced_content = core_service.generate_openai_response(prompt)
        
        return {"status": "success", "enhanced_content": enhanced_content}
    except Exception as e:
        logging.error(f"Error in enhance_application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))