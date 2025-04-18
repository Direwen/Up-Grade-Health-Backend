from chat_app.chatbot.state import State
from chat_app.chatbot.prompt_templates.task_manager_prompt_template import task_manager_prompt_template
from assistant.llm_clients import get_langchain_groq_client
import json

def task_manager(state: State):
    return {
        'response': get_langchain_groq_client().invoke(task_manager_prompt_template.format(
            username = state["username"],
            user_message = state["user_message"],
            health_conditions = ", ".join(state["health_conditions"]),
            health_restrictions = ", ".join(state["health_restrictions"]),
            previous_tasks = json.dumps(state["previous_tasks"], ensure_ascii=False),
            chat_history_summary = state["chat_history_summary"]
        ))
    }