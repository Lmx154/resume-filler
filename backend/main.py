from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import resume, system, application, settings  # Added settings
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
app.include_router(system.router)
app.include_router(application.router)
app.include_router(settings.router)  # <-- include settings router

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
