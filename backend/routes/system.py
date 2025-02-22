from fastapi import APIRouter
from services.file_service import file_service  # Correct import
from pydantic import BaseModel

router = APIRouter(prefix="/api/system", tags=["system"])

class FileRequest(BaseModel):
    file_path: str

@router.post("/read-file")
async def read_file(request: FileRequest):
    try:
        content = file_service.read_file_content(request.file_path)
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}