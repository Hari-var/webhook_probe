from database.database import db_dependency,get_db, sessionlocal # AsyncSessionLocal, 
from models.sql_request_response_models import ConfigDetailsRequest
from models.database_models.db_models import configDetails
# from models.sql_request_response_models import ConfigDetailsRequest as Approval
from datetime import datetime
import asyncio
from fastapi import Depends #type: ignore
from sqlalchemy.orm import Session
from typing import Annotated


async def save_approval(config_details:ConfigDetailsRequest) -> ConfigDetailsRequest:
    import uuid  # noqa: PLC0415
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