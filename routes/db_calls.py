from fastapi import APIRouter #type: ignore
from models.sql_request_response_models import ConfigDetailsRequest
from database.sql import save_approval

router = APIRouter()

@router.post("/save_config", response_model=ConfigDetailsRequest)
async def save_config(config_details: ConfigDetailsRequest):
    return await save_approval(config_details)