from fastapi import APIRouter
from services.system_service import system_service
from pydantic import BaseModel

router = APIRouter(prefix="/api/system", tags=["system"])

class FileRequest(BaseModel):
    file_path: str

@router.post("/read-file")
async def read_file(request: FileRequest):
    try:
        content = system_service.read_file_content(request.file_path)
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}
