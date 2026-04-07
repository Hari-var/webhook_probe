from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

LOG_FILE = Path("logs/app.log")


@router.get("/logs")
async def get_logs():
    if not LOG_FILE.exists():
        raise HTTPException(status_code=404, detail="Log file not found")

    return FileResponse(
        path=LOG_FILE,
        filename="app.log",
        media_type="text/plain"
    )