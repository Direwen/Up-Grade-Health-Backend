from chat_app.chatbot.state import State
from chat_app.chatbot.prompt_templates.router_prompt_template import router_prompt_template
from assistant.llm_clients import get_langchain_groq_client

def router(state: State) -> dict:
    node_destination = get_langchain_groq_client().invoke(router_prompt_template.format(user_message=state["user_message"])).content.strip()
    print(f"Router Node Destination: {node_destination}")
    return {"next": node_destination if node_destination in ["chatbot", "task_manager"] else "chatbot"}