from helpers.requester import get_data
import json


def parse_compare_response(compare_url, token=None):
    headers = {
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = get_data(compare_url, headers=headers)

    data = json.loads(response)

    parsed = {
        "summary": {
            "ahead_by": data.get("ahead_by"),
            "behind_by": data.get("behind_by"),
            "total_commits": data.get("total_commits"),
        },
        "files": [],
        "commits": []
    }

    # Parse files
    for file in data.get("files", []):
        parsed["files"].append({
            "filename": file.get("filename"),
            "status": file.get("status"),
            "additions": file.get("additions"),
            "deletions": file.get("deletions"),
            "changes": file.get("changes"),
            "patch": file.get("patch")
        })

    # Parse commits
    for commit in data.get("commits", []):
        parsed["commits"].append({
            "sha": commit.get("sha"),
            "message": commit.get("commit", {}).get("message"),
            "author": commit.get("commit", {}).get("author", {}).get("name"),
        })

    return parsed

if  __name__ == "__main__":
    compare_url = input("Enter compare URL: ")
    token = input("Enter GitHub token (optional): ")
    result = parse_compare_response(compare_url, token)
    print(json.dumps(result, indent=4))