from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import resume, application, settings  # Removed system
from config import settings as cfg

app = FastAPI(title=cfg.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing only, tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(resume.router)
app.include_router(application.router)
app.include_router(settings.router)  # Keep for API Key/Ollama settings

@app.get("/health")
async def health_check():
    return {"status": "healthy"}