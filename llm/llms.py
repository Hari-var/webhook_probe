import os
import google.generativeai as genai #type: ignore
import time
from dotenv import load_dotenv

def get_gemini_response(user_message):
    start_time = time.time()
    try:
        print("DEBUG: Loading .env file...")
        # Load .env from parent directory since we're in app/ folder
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(env_path)
        api=os.environ.get("Gemini_api_key")
        print(f"DEBUG: API key loaded: {'Yes' if api else 'No'}")
        print(f"DEBUG: API key length: {len(api) if api else 0}")
        if not api:
            print("DEBUG: Available environment variables:")
            for key in os.environ.keys():
                if 'gemini' in key.lower() or 'api' in key.lower():
                    print(f"  {key}")
        genai.configure(api_key=api)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(f"You are a PR reviewer. User: {user_message}")
        
        # Track metrics
        latency = time.time() - start_time
        print(latency)
        
        if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
            answer = response.candidates[0].content.parts[0].text
                        
            return answer
        else:
            return "Sorry, I couldn't get a response from Gemini. Please try again."
        
    except Exception as e:
        return f"Error: {str(e)}"