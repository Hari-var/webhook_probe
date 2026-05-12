import os
from dotenv import load_dotenv
load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
gemini_api_key = os.getenv("GEMINI_API_KEY")
cloud_db = os.getenv("cdb")
azure_ai_api_key = os.getenv("AZURE_AI_API_KEY")
azure_endpoint = "https://devops-maf2.openai.azure.com/"
azure_model = "Llama-4-Maverick-17B-128E-Instruct-FP8"
azure_api_version = "2024-05-01-preview"