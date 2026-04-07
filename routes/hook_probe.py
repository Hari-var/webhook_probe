from fastapi import APIRouter, Request 
from helpers.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()



@router.post("/webhook")
async def handle_webhook(request: Request):
    # Get the raw body
    body = await request.json()

    logger.info(f"Received webhook with body: {body}")
    
    
    # You can also access headers
    headers = dict(request.headers)
    print("Headers:", headers)
    
    return {"status": "success", 
            "received": True,
            "Raw body" : body,}
