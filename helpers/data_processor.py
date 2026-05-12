import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.requester import get_data
import json
from helpers.json_beautify import beautify_json


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

import json
import re


def text_to_json_v2(text: str) -> dict:
    """
    Convert mixed Python-style assignments to a Python dict.

    Handles:
    - Simple assignments:       KEY = "value" / KEY = True / KEY = 42
    - Inline JSON objects:      config = {"key": "value", ...}
    - Inline JSON arrays:       items = ["a", "b"]
    - Trailing comma values:    key = "value",
    - Multiple keys on one line: key1 = "v1", key2 = "v2"
    """
    result = {}

    # Normalize line endings and strip
    text = text.strip()

    # --- Pass 1: Extract block assignments (key = { ... } or key = [ ... ]) ---
    # Matches: identifier = { ... } or identifier = [ ... ] spanning content
    block_pattern = re.compile(
        r'([a-zA-Z_]\w*)\s*=\s*(\{[^}]*\}|\[[^\]]*\])',
        re.DOTALL
    )
    for match in block_pattern.finditer(text):
        key = match.group(1).strip()
        raw_value = match.group(2).strip()
        try:
            # JSON requires lowercase true/false — normalize Python booleans
            normalized = re.sub(r'\bTrue\b', 'true', raw_value)
            normalized = re.sub(r'\bFalse\b', 'false', normalized)
            normalized = re.sub(r'\bNone\b', 'null', normalized)
            result[key] = json.loads(normalized)
        except json.JSONDecodeError:
            result[key] = raw_value  # fallback: store as raw string

    # --- Pass 2: Extract simple key = value pairs (skip already matched blocks) ---
    # Remove block assignments from text before parsing simple pairs
    remaining = block_pattern.sub('', text)

    for raw_line in remaining.splitlines():
        # Split on comma to handle: key1 = "v1", key2 = "v2" on one line
        segments = raw_line.split(',')
        for segment in segments:
            segment = segment.strip()
            if not segment or segment.startswith('#') or '=' not in segment:
                continue

            key, _, raw_value = segment.partition('=')
            key = key.strip()
            raw_value = raw_value.strip().rstrip(',')  # strip trailing comma

            if not key or not re.match(r'^[a-zA-Z_]\w*$', key):
                continue  # skip malformed keys

            result[key] = _parse_scalar(raw_value)

    return result


def _parse_scalar(value: str):
    """Parse a single scalar value string into its Python type."""
    # Quoted string — single or double
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]

    # Boolean
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False

    # Null
    if value.lower() in ('none', 'null'):
        return None

    # Number
    try:
        return float(value) if '.' in value else int(value)
    except ValueError:
        pass

    # Fallback — return as-is
    return value

if  __name__ == "__main__":
    # compare_url = input("Enter compare URL: ")
    # token = input("Enter GitHub token (optional): ")
    # result = parse_compare_response(compare_url, token)
    # print(json.dumps(result, indent=4))
    with open("trail.txt", "r") as file:
        text = file.read()
    print(text)
    print("=" * 20)
    # result = text_to_json_v2(text)
    result = json.loads((text))
    print(json.dumps(result, indent=4))
