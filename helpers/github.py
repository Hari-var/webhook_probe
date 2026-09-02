import httpx
import asyncio
from helpers.config import github_token
from helpers.logger import get_logger

logger = get_logger(__name__)

async def store_webhook_response(repo_name: str, commit_sha: str, payload: dict):
    import base64, json
    path = f"hook_responses/{repo_name}/{commit_sha}.json"
    url = f"https://api.github.com/repos/Hari-var/test1/contents/{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    content = base64.b64encode(json.dumps(payload, indent=2).encode()).decode()

    async with httpx.AsyncClient() as client:
        get_resp = await client.get(url, headers=headers)
        if get_resp.status_code == 200:
            existing_sha = get_resp.json().get("sha")
            body = {"message": f"update webhook response for {commit_sha}", "content": content, "sha": existing_sha}
        else:
            body = {"message": f"store webhook response for {commit_sha}", "content": content}
        response = await client.put(url, headers=headers, json=body)

    logger.info(f"Stored webhook response: {response.status_code} - {response.text}")
    return response.json()


async def add_pr_comment(
    owner,
    repo,
    pull_number,
    commit_id,
    path,
    line,
    body,
    start_side="RIGHT",
    side="RIGHT",
):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews"

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

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
    logger.info(f"PR-comment added response: {response}")

    return response.json()

if __name__ == "__main__":
    owner = input("Enter repo owner: ")
    repo = input("Enter repo name: ")
    pull_number = int(input("Enter pull request number: "))
    commit_id = input("Enter commit ID: ")
    path = input("Enter file path for comment: ")
    body = input("Enter comment body: ")
    line = int(input("Enter line number for comment: "))

    response = asyncio.run(
        add_pr_comment(
            owner=owner,
            repo=repo,
            pull_number=pull_number,
            commit_id=commit_id,
            path=path,
            line=line,
            body=body
        )
    )
    print("Comment added:", response)