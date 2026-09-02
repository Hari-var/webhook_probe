import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import google.generativeai as genai #type: ignore
import time
from helpers.config import azure_ai_api_key, azure_endpoint, azure_model, azure_api_version
# from dotenv import load_dotenv

# def get_gemini_response(user_message):
#     start_time = time.time()
#     try:
#         print("DEBUG: Loading .env file...")
#         # Load .env from parent directory since we're in app/ folder
#         env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
#         load_dotenv(env_path)
#         api=os.environ.get("Gemini_api_key")
#         print(f"DEBUG: API key loaded: {'Yes' if api else 'No'}")
#         print(f"DEBUG: API key length: {len(api) if api else 0}")
#         if not api:
#             print("DEBUG: Available environment variables:")
#             for key in os.environ.keys():
#                 if 'gemini' in key.lower() or 'api' in key.lower():
#                     print(f"  {key}")
#         genai.configure(api_key=api)
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         response = model.generate_content(f"You are a PR reviewer. User: {user_message}")
        
#         # Track metrics
#         latency = time.time() - start_time
#         print(latency)
        
#         if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
#             answer = response.candidates[0].content.parts[0].text
                        
#             return answer
#         else:
#             return "Sorry, I couldn't get a response from Gemini. Please try again."
        
#     except Exception as e:
#         return f"Error: {str(e)}"
    
from openai import AzureOpenAI #type: ignore

def get_azure_response(text):
    try:
        endpoint = azure_endpoint
        deployment = azure_model
        subscription_key = azure_ai_api_key
        api_version = azure_api_version
        print(endpoint, deployment, subscription_key, api_version)
        if not subscription_key:
            return "Error: AZURE_OPENAI_KEY not found in environment variables"
 
        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=subscription_key,
        )
 
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            max_tokens=1000,
            temperature=0.7,
            model=deployment
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Azure Error: {str(e)}"

if __name__ == "__main__":
    print(get_azure_response("Hello, how are you?"))