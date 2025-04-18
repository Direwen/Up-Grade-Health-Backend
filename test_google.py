from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

try:
    client = genai.Client(
        api_key=os.environ.get("GOOGLE_API_KEY")
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents="What's the difference between agentic AI and non-agentic AI?",
    )
    print(response.text)
except Exception as err:
    print(f"Error: {err}")
