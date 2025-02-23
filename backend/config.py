from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import logging
from pydantic import Field

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Resume Filler"
    debug: bool = False
    frontend_url: str = "http://localhost:5173"
    openai_api_key: str = ""
    openai_api_base: str = ""
    ollama_base_url: str = "http://localhost:11434"
    model: str = "gpt-4o-mini"  # Default model updated to "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
logging.info(f"Loaded OPENAI_API_KEY (first 4 chars): {settings.openai_api_key[:4] if settings.openai_api_key else 'None'}")
logging.info(f"Loaded OPENAI_API_BASE: {settings.openai_api_base}")
logging.info(f"Loaded OPENAI model: {settings.model}")