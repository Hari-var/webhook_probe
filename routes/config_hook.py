import re
import os
import httpx
import requests
from fastapi import APIRouter, HTTPException, Request #type: ignore
from json import loads
from database.sql import save_approval
from helpers.data_processor import text_to_json
from models.config_validator_model import ConfigValidator
from models.sql_request_response_models import ConfigDetailsRequest
from helpers.json_beautify import beautify_json
import json

router = APIRouter()



_CONFIG_PATTERN = re.compile(r'.*config.*\.json$')

def _find_config_file(commits: list) :
    changed_files = [file for commit in commits for file in commit.get("modified", []) + commit.get("added", [])]

    # iterate over all changed files to find a config file
    for file in changed_files:
        if _CONFIG_PATTERN.search(file):
            return file, changed_files
    return None, changed_files


@router.post("/run_flow2")
async def run_flow2(request: Request):
    print(request)
    data = await request.json()
    print(data)
    commits = data.get("commits", [])
    repo_name = data.get("repository", {}).get("full_name", "")
    ref = data.get("ref", "").replace("refs/heads/", "")
    head_commit = data.get("head_commit", {})

    config_file, changed_files = _find_config_file(commits)
    if not config_file:
        return {"message": "No config file found"}

    raw_url = f"https://raw.githubusercontent.com/{repo_name}/{ref}/{config_file}"

    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(raw_url)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Failed to fetch config file: {response.status_code}")
    raw_config = json.dumps(response.text, indent=4)
    try:
        validated_config = ConfigValidator(**json.loads(raw_config))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid config format: {e}")

    payload = ConfigDetailsRequest(
        repo=repo_name,
        branch=ref,
        status="pending",
        commit_sha=head_commit.get("id", ""),
        commit_message=head_commit.get("message", ""),
        committed_by=head_commit.get("pusher", {}).get("name", ""),
        committed_at=head_commit.get("timestamp", ""),
        changed_files=changed_files,
        config=validated_config.config,
        techstack=validated_config.techstack,
        startup_command=validated_config.startup_command,
        startup_command_filepath=validated_config.startup_command_filepath,
        created_at=head_commit.get("timestamp", ""),
        created_by=head_commit.get("pusher", {}).get("name", "")
    )
    # payload = {
    #     "repo": repo_name,
    #     "branch": ref,
    #     "status": "pending",
    #     "commit_sha": head_commit.get("id", ""),
    #     "commit_message": head_commit.get("message", ""),
    #     "committed_at": head_commit.get("timestamp", ""),
    #     "committed_by": head_commit.get("pusher", {}).get("name", ""),
    #     "changed_files": changed_files,
    #     "config": text_to_json(response.text),
    # }
    await save_approval(config_details=payload)
    # config_data = loads(response.text)
    return {
        "message": "Config file found",
        "payload": payload,
    }




if __name__ == "__main__":
    url=input("Enter the URL: ")
    response = requests.get(url)
    print(text_to_json(response.text))