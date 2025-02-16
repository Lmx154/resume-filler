from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Resume Filler"
    debug: bool = False
    frontend_url: str = "http://localhost:5173"
    openai_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
