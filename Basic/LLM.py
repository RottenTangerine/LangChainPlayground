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
