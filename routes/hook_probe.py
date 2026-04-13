from fastapi import APIRouter, Request 
from helpers.logger import get_logger
import requests
from helpers.data_processor import parse_compare_response
from helpers.requester import get_data
from llm.llms import get_gemini_response
from helpers.promptManager import PromptManager
from helpers.github import add_pr_comment

from helpers.models import WebhookPayload, LLMResponse

logger = get_logger(__name__)

router = APIRouter()



@router.post("/webhook")
async def handle_webhook(request: Request):
    # Get the raw body
    body = await request.json()
    payload = WebhookPayload(**body)
    logger.info(f"Received webhook with body: {body}")
    if payload.action != "opened":
        return {"status": "ignored"}
    
    pr = payload.pull_request
    repo = payload.repository

    repo_owner = repo.owner.login
    repo_name = repo.name

    head_sha = pr.head.sha
    base_sha = pr.base.sha

    compare_url = repo.compare_url.replace("{base}", base_sha).replace("{head}", head_sha)

    diff_data = get_data(pr.diff_url)
    compare_data = parse_compare_response(compare_url)

    # pull_request = body.get("pull_request")
    # logger.info(f"Pull request opened: {pull_request.get('title')}")
    # pr_id = pull_request.get("id")
    # pr_state = pull_request.get("state")
    # pr_title = pull_request.get("title")
    # pr_body =  pull_request.get("body")
    # pr_locked = pull_request.get("locked")
    # pr_comments_url = pull_request.get("comments_url")

    # user = pull_request.get("user")
    # user_login = user.get("login")
    # user_id = user.get("id")
    # user_type = user.get("type")
    # user_view_type = user.get("user_view_type")
    # user_site_admin = user.get("site_admin")

    # repo = body.get("repository")
    # repo_owner = repo.get("owner").get("login")
    # repo_id = repo.get("id")
    # repo_name = repo.get("name")
    # repo_private = repo.get("private")
    # repo_diff_url = repo.get("diff_url")

    # head = pull_request.get("head")
    # head_ref = head.get("ref")
    # head_sha = head.get("sha")

    # base = pull_request.get("base")
    # base_ref = base.get("ref")
    # base_sha = base.get("sha")

    # compare_URL_template = repo.get("compare_url")
    # compare_URL = compare_URL_template.replace("{base}", base_sha).replace("{head}", head_sha)
    
    # pr_metadata = {
    #     "id": pr_id,
    #     "state": pr_state,
    #     "title": pr_title,
    #     "body": pr_body,
    #     "locked": pr_locked,
    #     "comments_url": pr_comments_url,
    #     "user": {
    #         "login": user_login,
    #         "id": user_id,
    #         "type": user_type,
    #         "user_view_type": user_view_type,
    #         "site_admin": user_site_admin
    #     },
    #     "repository": {
    #         "id": repo_id,
    #         "name": repo_name,
    #         "private": repo_private,
    #         "diff_url": repo_diff_url
    #     },
    #     "head": {
    #         "ref": head_ref,
    #         "sha": head_sha
    #     },
    #     "base": {
    #         "ref": base_ref,
    #         "sha": base_sha
    #     }
    # }
    # diff_data = get_data(repo_diff_url)
    # compare_data = parse_compare_response(compare_URL)

    pm = PromptManager()
    prompt = pm.format("pr_review", PR_METADATA=pr.model_dump(), COMPARE_DATA=compare_data, DIFF_DATA=diff_data)

    response =  get_gemini_response(prompt)
    logger.info("Gemini response:", response)
    from json import loads
    parsed = LLMResponse(**loads(
        response.replace("```json", "").replace("```", "")
    ))
    for comment in parsed.comments:
        await add_pr_comment(
            owner=repo_owner,
            repo=repo_name,
            pull_number=payload.number,
            commit_id=head_sha,
            path=comment.path,
            line=comment.line,
            body=comment.body,
            start_line=comment.start_line,
            start_side="Right",
            side="Right",
        )

    
    return {"status": "success", 
            "received": True,
            "Raw body" : pr.model_dump(),}
