import os
import openai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

try:
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": """You are the user health profile builder. Your job is to Extract 'conditions' and 'restrictions' from the user's health description in JSON format. Example: Input: "I have diabetes and am allergic to peanuts." Output: {"conditions": ["diabetes"], "restrictions": ["peanuts"]}""",
            },
            {
                "role": "user",
                "content": """The user is a 20-year-old individual, standing at 5'5", who is currently focused on improving their health and fitness by regularly going to the gym. They appear to maintain an active lifestyle and are mindful of their physical well-being. The user has a history of seasonal allergies and is mildly allergic to shellfish. They also manage mild asthma, which is triggered occasionally by cold weather or intense exercise."""
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object"
        }
    )
    
    print(response.choices[0].message.content)
except Exception as err:
    print(f"Error: {err}")
finally:
    print("Request Completed")