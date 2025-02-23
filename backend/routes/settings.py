from fastapi import APIRouter
from pydantic import BaseModel
from services.config_service import config_service
from services.core_service import core_service

router = APIRouter(prefix="/api/settings", tags=["settings"])

class OpenAISettings(BaseModel):
    api_base: str
    api_key: str
    model: str  # Add model field

@router.get("/openai")
def get_openai_settings():
    config = config_service.load_config()
    return {
        "api_base": config.get("api_base", ""),
        "api_key": config.get("api_key", ""),
        "model": config.get("model", "gpt-3.5-turbo-16k")  # Default model
    }

@router.post("/openai")
def save_openai_settings(settings: OpenAISettings):
    try:
        config_service.update_config("api_base", settings.api_base)
        config_service.update_config("api_key", settings.api_key)
        config_service.update_config("model", settings.model)
        core_service.init_openai(settings.api_key, settings.api_base)  # Reinitialize client, model handled in core_service
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}