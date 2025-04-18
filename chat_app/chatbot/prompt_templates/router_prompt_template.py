from langchain_core.prompts import PromptTemplate

router_prompt_template = PromptTemplate.from_template(
    """
    You are a routing assistant. Analyze the user's message and decide whether it is:
    - A general health-related question (route to "chatbot"), or
    - A request for tasks of the day or to modify assigned tasks (route to "task_manager").

    If the message contains both, route to "task_manager".
    
    Respond with only one of the following:
    - "chatbot"
    - "task_manager"

    ### Examples:

    User's Message: "Can you explain why hydration is important?"
    Output: chatbot

    User's Message: "I want to change one of the tasks you gave me earlier."
    Output: task_manager

    User's Message: "Can I get some new tasks for today?"
    Output: task_manager

    User's Message: "Is it safe to exercise with high blood pressure?"
    Output: chatbot

    User's Message: "I’m not sure about that walking task. Can we switch it?"
    Output: task_manager
    
    User's Message: "I meant the third task from your last generated tasks for modification"
    Output: task_manager

    ### User Input:

    User's Message: {user_message}
    Output:
    """
)
