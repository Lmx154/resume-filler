from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.core_service import application_service, last_extraction
import logging

router = APIRouter(prefix="/api/application", tags=["application"])

class ExtractRequest(BaseModel):
    text: str

@router.post("/extract")
async def extract_application(request: ExtractRequest):
    try:
        logging.info("Received extraction request")
        result = application_service.process_extracted_text(request.text)
        logging.info(f"Result: {result['status']}")
        
        # Verify the global variable is updated
        global last_extraction
        if last_extraction != result:
            logging.warning("last_extraction not updated properly")
        
        return result
    except Exception as e:
        logging.error(f"Error in extract_application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/last_extract")
async def get_last_extraction():
    global last_extraction
    logging.info(f"Getting last extraction. Full content: {last_extraction}")
    
    if not last_extraction:
        logging.warning("No extraction data available")
        return {"status": "pending", "message": "No extraction data available"}
        
    if 'status' not in last_extraction or 'display_text' not in last_extraction:
        logging.error(f"Invalid last_extraction structure: {last_extraction.keys()}")
        return {"status": "error", "message": "Invalid data structure"}
    
    logging.info(f"Returning extraction with text length: {len(last_extraction.get('display_text', ''))}")    
    return last_extraction
