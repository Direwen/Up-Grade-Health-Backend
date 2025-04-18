from typing import TypedDict, List

class State(TypedDict):
    username: str
    user_message: str
    health_conditions: list
    health_restrictions: list
    chat_history_summary: str
    previous_tasks: List[dict]
    response: str