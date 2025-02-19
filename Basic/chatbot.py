from icecream import ic

import json

# load config
with open("../config.json", 'r') as f:
    config = json.load(f)

auth = config.get('DS')

# Set up llm model
from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(
    api_key=auth.get("key"),
    model="deepseek-chat"
)


# Pass the entire conversation history into the model
# Message persistence - (langGraph)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

