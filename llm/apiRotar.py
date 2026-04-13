import os
from dotenv import load_dotenv

CURRENT_API_INDEX = 0
API_KEYS = []

def load_api_keys():
    global API_KEYS
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
    
    keys = []
    for i in range(1, 10):  # Check for up to 10 API keys
        key_name = f"Gemini_api_key_{i}" if i > 1 else "Gemini_api_key"
        key = os.environ.get(key_name)
        if key:
            keys.append(key)
    
    API_KEYS = keys
    return keys

def get_next_api_key():
    global CURRENT_API_INDEX
    if not API_KEYS:
        load_api_keys()
    
    if not API_KEYS:
        return None
    
    key = API_KEYS[CURRENT_API_INDEX]
    CURRENT_API_INDEX = (CURRENT_API_INDEX + 1) % len(API_KEYS)
    return key
