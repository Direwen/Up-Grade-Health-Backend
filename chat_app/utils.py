from openai import OpenAI
from langgraph.graph import StateGraph
import json

def summarize_chat_history(client : OpenAI, messages: list, model : str = "bytedance-research/ui-tars-72b:free") -> str:
    
    system_message = {
        "role": "system",
        "content": """
        You are a bot whose only job is to distill the list of chat messages between a user and an assistant, 
        which user will provide, into a single summary message with these requirements:
        - Covers the entire conversation in chronological order (from oldest to newest),
        - Includes as many specific details as possible,
        - Avoids omitting important facts or decisions made during the conversation.
        The provided list of messages starts from newest to oldest messages and includes roles and content in each dictionary.
        Retain the original flow of the dialogue, and ensure your summary reflects the full context accurately.
        If the provided list is empty, just reply with "No Chat History".
        If there are repetitive task generations, consider only the most recent one into summarization.
        """
    }
    
    user_message = {
        "role": "user",
        "content": json.dumps(messages)
    }
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                system_message,
                user_message
            ]
        ).choices[0].message.content
        
        print(f"Summary: {response}")
        
        return response
    except:
        return ""

def format_chat_history(messages):
    formatted_messages = []
    for message in messages:
        role = "user" if message.is_user else "assistant"
        formatted_messages.append({
            "role": role,
            "content": message.content
        })
    return formatted_messages

def test_app(
    app: StateGraph,
    username: str,
    user_message: str,
    conditions: list,
    restrictions: list,
    previous_tasks: list,
    chat_history_summary: str
):
    return app.invoke({
        "username": username,
        "user_message": user_message,
        "health_conditions": conditions,
        "health_restrictions": restrictions,
        "previous_tasks": previous_tasks,
        "chat_history_summary": chat_history_summary
    })['response'].content
    