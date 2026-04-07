from fastapi import FastAPI, Request 
from fastapi.middleware import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Get the raw body
    body = await request.json()
    
    
    # You can also access headers
    headers = dict(request.headers)
    print("Headers:", headers)
    
    return {"status": "success", 
            "received": True,
            "Raw body" : body,}
