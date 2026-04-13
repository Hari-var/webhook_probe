import os
from dotenv import load_dotenv
load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
gemini_api_key = os.getenv("GEMINI_API_KEY")