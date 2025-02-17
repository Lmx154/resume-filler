from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import resume, system, application
from config import settings

app = FastAPI(title=settings.app_name)

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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
