import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_groq import ChatGroq

load_dotenv()

openrouter_client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.environ.get("OPENROUTER_API_KEY")
)

groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)


def get_langchain_groq_client(model_name : str="llama-3.3-70b-versatile") -> ChatGroq:
    return ChatGroq(
        model=model_name,
        api_key=os.getenv("GROQ_API_KEY")
    )