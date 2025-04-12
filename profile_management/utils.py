def extract_health_conditions(client, health_description):
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": """You are the user health profile builder. Your job is to Extract 'conditions' and 'restrictions' from the user's health description in JSON. Example: Input: "I have diabetes and am allergic to peanuts." Output: {"conditions": ["diabetes"], "restrictions": ["peanuts"]}""",
                },
                {
                    "role": "user",
                    "content": health_description
                }
            ],
            temperature=0,
            response_format={
                "type": "json_object"
            }
        )
    
        return response.choices[0].message.content
    
    except Exception as err:
        return None