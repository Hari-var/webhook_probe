import httpx
import asyncio
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