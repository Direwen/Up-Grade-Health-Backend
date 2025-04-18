from langgraph.graph import StateGraph, END, START
from .state import State
from chat_app.chatbot.nodes import router_node, chatbot_node, task_manager_node

#Initialize State Graph
graph = StateGraph(State)
graph.add_node('router', router_node.router)
graph.add_node('chatbot', chatbot_node.chatbot)
graph.add_node('task_manager', task_manager_node.task_manager)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    'router',
    lambda x: x["next"],
    {
        "chatbot": 'chatbot',
        "task_manager": 'task_manager'
    }
)
graph.add_edge('chatbot', END)
graph.add_edge('task_manager', END)
app = graph.compile()