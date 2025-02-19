from icecream import ic
from LLM import model

# invoke message
from langchain_core.messages import HumanMessage, SystemMessage
prompt = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]


# response = model.invoke(prompt)
# ic(response)
#
# ## Stream mode
# for chunk in model.stream(prompt):
#     ic(chunk.content, end="|")


# Prompt Template
from langchain_core.prompts import ChatPromptTemplate
system_template = "Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

prompt = prompt_template.invoke({"language": "Italian", "text": "hi!"})
ic(prompt)

prompt_message = prompt.to_messages()
ic(prompt_message)

response = model.invoke(prompt_message)
ic(response)