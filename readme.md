# LangChain

This repo. is for testing the LangChain features base on online tutorials.

Have fun

# Docs:

[LangChain Doc](https://python.langchain.com/docs/introduction/)

[Integration Doc](https://python.langchain.com/docs/integrations/providers/)


Official Tutorials:
[LangChain Adademy](https://academy.langchain.com/)

Github: 
[langchain-ai/langchain-academy](https://github.com/langchain-ai/langchain-academy)

# Tutorials

- Create `config.json`

config.json:
```json
{
  "DS": {
    "endpoint": "https://api.deepseek.com",
    "key": "YOUR_API_KEY",
    "model": "deepseek-chat"
  },
  "Qwen": {
    "endpoint": "YOUR_ENDPOINT",
    "key": "YOUR_API_KEY",
    "model": "DeepSeek-R1-Distill-Qwen-32B"
  }
}
```

- Modify utils/LLM.py
```python
# Modify this part

auth = config.get('DS')

# Set up llm model
from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(
    api_key=auth.get("key"),
    model="deepseek-chat"
)
```

---

# Notes


# LCEL

链式语言LCEL (LangChain Execution Language)

```
r1 | r2 | r3
```

把各种各样的大模型/工具统一进行异步调用

```python
result = model.invoke(messages)
response = parser.invoke(result)


chain = model | parser
response = chain.invoke(messages)
```

使用LCEL创建的链实现了整个标准的Runnable接口

# Stream mode

底层原理是用了服务器端SSE(事件机制)技术,进行一个长链接,建立HTTP通道,发送事件

# 组件

LangChain组件(实现Runnable协议)标准接口

- stream
- invoke
- batch

异步方法**应该与asyncio一起使用`await`语法实现**

- astream
- ainvoke
- abatch
- astream_log
- astream_evevts

| Component     | Input                            | output                 |
| ------------- | -------------------------------- | ---------------------- |
| Prompt        | dict                             | prompt message         |
| Chat Model    | string, list[string]             | chat message (json)    |
| LLM           | string, list[string]             | string                 |
| Output parser | chat message, string             | depends on parser type |
| Retriever     | string                           | Doc. list              |
| Tools         | string / string depends on tools | depends on tools       |

## Input / Output check

Pydantic

- input_schema
- output_schema

# LangGraph

# Concepts

## Graph

To build your graph, you first define the **state**, you then add **nodes** and **edges**, and then you compile it.
### State

> The State consists of the schema of the graph as well as reducer functions which specify how to apply updates to the state. The schema of the State will be the input schema to all Nodes and Edges in the graph, and can be either a TypedDict or a Pydantic model. All Nodes will emit updates to the State which are then applied using the specified reducer function.

#### State Schema

> These are type hints. they are not enforced at runtime!

**TypedDict**

```python
from typing import Literal

class TypedDictState(TypedDict):
    name: str
    mood: Literal["happy","sad"]
```

**Dataclass**

Python's dataclasses provide another way to define structured data.
Dataclasses offer a concise syntax for creating classes that are primarily used to store data.

```python
from dataclasses import dataclass

@dataclass
class DataclassState:
    name: str
    mood: Literal["happy","sad"]
```

**Pydyntic**

`TypedDict` and `dataclasses` provide type hints but they don't enforce types at runtime. 

This means you could potentially assign invalid values without raising an error!

```python
from pydantic import BaseModel, field_validator, ValidationError

class PydanticState(BaseModel):
    name: str
    mood: str # "happy" or "sad" 

    @field_validator('mood')
    @classmethod
    def validate_mood(cls, value):
        # Ensure the mood is either "happy" or "sad"
        if value not in ["happy", "sad"]:
            raise ValueError("Each mood must be either 'happy' or 'sad'")
        return value

try:
    state = PydanticState(name="John Doe", mood="mad")
except ValidationError as e:
    print("Validation Error:", e)
```

> Otuput:
>
> Validation Error: 1 validation error for PydanticState
> mood
>   Input should be 'happy' or 'sad' [type=literal_error, input_value='mad', input_type=str]
>     For further information visit https://errors.pydantic.dev/2.8/v/literal_error

#### Reducers

**Default (overwriting)**

```python
class State(TypedDict):
    foo: int
```

**With Reducers**

We use the `Annotated` type to specify a reducer function. They specify how to perform updates.

```python
from operator import add
from typing import Annotated

class State(TypedDict):
    foo: Annotated[list[int], add]
```

**More customized**

```python
def reduce_list(left: list | None, right: list | None) -> list:
    """Safely combine two lists, handling cases where either or both inputs might be None.

    Args:
        left (list | None): The first list to combine, or None.
        right (list | None): The second list to combine, or None.

    Returns:
        list: A new list containing all elements from both input lists.
               If an input is None, it's treated as an empty list.
    """
    if not left:
        left = []
    if not right:
        right = []
    return left + right

class DefaultState(TypedDict):
    foo: Annotated[list[int], add]

class CustomReducerState(TypedDict):
    foo: Annotated[list[int], reduce_list]
```

### Node

> nodes are typically python functions (sync or async) where the first positional argument is the state, and (optionally), the second positional argument is a "config", containing optional configurable parameters (such as a thread_id).

Add Node

```python
graph.addnode(node)
```

Special Nodes

```python
from langgraph.graph import START, END
```
### Edge

A node can have **MULTIPLE** outgoing edges. If a node has multiple out-going edges, all of those destination nodes will be executed in parallel as a part of the next superstep.


Normal Edge

```python
graph.add_edge("node_a", "node_b")
```

Conditional Edge

```python
graph.add_conditional_edges("node_a", routing_function, {True: "node_b", False:"node_c"})
```


# LangServe (Deprecated)

Now integrated in LangGraph Platform

See: LangGraph/Deployments

```
pip install --upgrade "langserve[all]"

or:
client side: pip install "langserve[client]"
server side; pip install "langserve[server]"
```

## LangChain CLI

使用LangChain CLI快速启动LangServe项目

```
pip install -U langchain-cli
```

创建新应用

```
langchain app new langserve
```