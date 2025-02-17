from fastapi import APIRouter
from pydantic import BaseModel
from services.config_service import config_service
from services.ai_service import ai_service

router = APIRouter(prefix="/api/settings", tags=["settings"])

class OpenAISettings(BaseModel):
    api_base: str
    api_key: str

@router.get("/openai")
async def get_openai_settings():
    config = config_service.load_config()
    return {
        "api_base": config.get("api_base", ""),
        "api_key": config.get("api_key", "")
    }

@router.post("/openai")
async def save_openai_settings(settings: OpenAISettings):
    try:
        config_service.update_config("api_base", settings.api_base)
        config_service.update_config("api_key", settings.api_key)
        
        # Initialize AI service with new settings
        ai_service.init_openai(settings.api_key, settings.api_base)
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
