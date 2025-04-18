from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/nebius/v1",
    api_key=os.environ.get('HUGGINGFACE_API_KEY')
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3-0324-fast",
    messages=[
        {
            "role": "user",
            "content": "What's agentic AI?"
        }
    ],
    max_tokens=512,
)

print(completion.choices[0].message.content)