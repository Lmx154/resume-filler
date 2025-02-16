from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import resume, system
from config import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(system.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
