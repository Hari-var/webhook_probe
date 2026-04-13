import httpx
from helpers.config import github_token
from helpers.logger import get_logger

logger = get_logger(__name__)

async def add_pr_comment(
    owner,
    repo,
    pull_number,
    commit_id,
    path,
    line,
    body,
    start_line=None,
    start_side="RIGHT",
    side="RIGHT",
):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    payload = {
        "body": body,
        "commit_id": commit_id,
        "path": path,
        "line": line,
        "side": side,
    }

    if start_line:
        payload["start_line"] = start_line
        payload["start_side"] = start_side

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
    logger.info(f"PR-comment added response: {response}")

    return response.json()