from fastapi import FastAPI #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from routes import hook_probe, logs, config_hook, db_calls
import models.DB_model as model
from database.database import engine


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

model.Base.metadata.create_all(bind=engine) #type: ignore

app.include_router(logs.router, prefix="/logs", tags=["logs"])
app.include_router(hook_probe.router, prefix="/probe", tags=["webhook"])  # Assuming 'router' is defined in hook_probe.py
app.include_router(config_hook.router, prefix="/config_hook", tags=["config-hook"])
app.include_router(db_calls.router, prefix="/db", tags=["database"])