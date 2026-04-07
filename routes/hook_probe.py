from fastapi import APIRouter, Request 


router = APIRouter()



@router.post("/webhook")
async def handle_webhook(request: Request):
    # Get the raw body
    body = await request.json()
    
    
    # You can also access headers
    headers = dict(request.headers)
    print("Headers:", headers)
    
    return {"status": "success", 
            "received": True,
            "Raw body" : body,}
