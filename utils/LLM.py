import json
import os

path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(os.path.dirname(path), 'config.json')

# load config
with open(config_path, 'r') as f:
    config = json.load(f)

auth = config.get('DS')

# Set up llm model
from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(
    api_key=auth.get("key"),
    model="deepseek-chat"
)
