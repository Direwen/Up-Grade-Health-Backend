import os
import openai
from dotenv import load_dotenv

def get_openai_client():
    # Load enviroment variables from .env file
    load_dotenv()
    # Get API Key from env file
    api_key = os.getenv("GROQ_API_KEY")
    # Create OPENAI client
    return openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY")
    )