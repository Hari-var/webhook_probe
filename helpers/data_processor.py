from helpers.requester import get_data
import json


def parse_compare_response(compare_url, token=None):
    headers = {
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = get_data(compare_url, headers=headers)
    response = " " if response is None else response

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

def text_to_json(text):
    """
    Convert Python-style variable assignments in a string to JSON.
    
    Example input:
    TENANT_ID = "abc"
    ENABLE_SAST = True
    """
    config = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # skip empty lines and comments
        if "=" not in line:
            continue  # skip invalid lines
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        
        # Convert string values
        if value.startswith('"') and value.endswith('"') or value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        # Convert booleans
        elif value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        # Convert numbers
        else:
            try:
                if "." in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  # leave as string if cannot parse
        
        config[key] = value
    
    return json.dumps(config, indent=4)

if  __name__ == "__main__":
    compare_url = input("Enter compare URL: ")
    token = input("Enter GitHub token (optional): ")
    result = parse_compare_response(compare_url, token)
    print(json.dumps(result, indent=4))