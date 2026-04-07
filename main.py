from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import hook_probe, logs

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(hook_probe.router, prefix="/probe", tags=["webhook"])  # Assuming 'router' is defined in hook_probe.py