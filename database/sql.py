from database.database import db_dependency,get_db, sessionlocal # AsyncSessionLocal, 
from models.sql_request_response_models import ConfigDetailsRequest
from models.database_models.db_models import configDetails
from models.database_models.pr_review_details import PrDetails
# from models.sql_request_response_models import ConfigDetailsRequest as Approval
from datetime import datetime
import asyncio
from fastapi import Depends #type: ignore
from sqlalchemy.orm import Session
from typing import Annotated
import uuid 
import requests

async def save_approval(config_details:ConfigDetailsRequest) -> ConfigDetailsRequest:
     # noqa: PLC0415
    try:
        db_obj = configDetails(
        **config_details.model_dump()
    )
        db = sessionlocal()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except asyncio.CancelledError:
        # Don't suppress cancellation, but ensure clean state
        raise
    except Exception:
        # Handle other database errors
        raise
    return config_details

async def save_pr_review_details(pr_details: dict):
    try:
        db_obj = PrDetails(
            **pr_details
        )
        db = sessionlocal()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except asyncio.CancelledError:
        # Don't suppress cancellation, but ensure clean state
        raise
    except Exception:
        # Handle other database errors
        raise