from chat_app.chatbot.state import State
from chat_app.chatbot.prompt_templates.chatbot_prompt_template import chatbot_template
from assistant.llm_clients import get_langchain_groq_client

def chatbot(state: State):
    return {
        "response": get_langchain_groq_client().invoke(chatbot_template.format(user_message=state["user_message"]))
    }