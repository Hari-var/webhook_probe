

from fastapi import APIRouter, HTTPException #type: ignore
from models.sql_request_response_models import ConfigDetailsRequest
from database.sql import save_approval, save_pr_review_details
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter()

@router.post("/save_config", response_model=ConfigDetailsRequest)
async def save_config(config_details: ConfigDetailsRequest):
    return await save_approval(config_details)


# Define a Pydantic model for PR review details (adjust fields as needed)
class PrReviewDetailsRequest(BaseModel):
    repo: str
    branch: str
    commit_sha: str
    commit_message: Optional[str] = ""
    committed_by: Optional[str] = ""
    committed_at: str
    changed_files: List[Any] = []
    pr_id: Optional[int] = None
    pr_title: Optional[str] = ""
    pr_body: Optional[str] = ""
    pr_state: Optional[str] = ""
    pr_locked: Optional[int] = 0
    pr_comments_url: Optional[str] = ""
    user_login: Optional[str] = ""
    user_id: Optional[int] = None
    user_type: Optional[str] = ""
    user_site_admin: Optional[int] = 0
    head_ref: Optional[str] = ""
    base_ref: Optional[str] = ""
    config: Optional[Dict[str, Any]] = {}
    diff_details: Optional[str] = ""
    pr_review_comments: List[Any] = []
    status: Optional[str] = "pending"
    created_at: str
    created_by: Optional[str] = ""
    updated_at: Optional[str] = None
    updated_by: Optional[str] = ""

@router.post("/save_pr_review_details")
async def save_pr_review_details_endpoint(pr_details: PrReviewDetailsRequest):
    try:
        result = await save_pr_review_details(pr_details.dict())
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save PR review details: {e}")