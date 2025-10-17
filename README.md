<p align="center">
  <a href="https://embedia.ai">
    <img src="https://embedia-website-kohl.vercel.app/logo.png" height="64">
    <h3 align="center">Embedia</h3>
  </a>
</p>

<p align="center">
  Make LLM-powered webapps with ease
</p>

<p align="center">
  <a href="https://embedia-ai.vercel.app/docs"><strong>Docs</strong></a>
</p>
<br/>

## What is Embedia?

Embedia is a framework for making LLM-powered webapps with ease.

With `Python 3.8` or higher set up, install Embedia using:

```bash
pip install embedia
```

## Which webapps can be created using Embedia?

Embedia is built keeping in mind the common as well as advanced usecases of LLMs
in webapps.

Some advanced usecases include:

- **AI Agents** that can **run predefined code** with **custom parameters**
  based on **conversation context**
- **Natural language search** over files, websites, or datasets powered by
  **Retrieval Augmented Generation**
- **Coding assistants** that can **translate, write, run, test, and debug code**
- All the **functionalities of OpenAI ChatGPT**, but with an **opensource LLM**
  like llama-2

Some common usecases include:

- Chatbots with a personality (similar to
  [character.ai](https://beta.character.ai/))
- A panel discussion between multiple personalities. These multiple
  personalities can also be internal to a single complex chatbot.
- Language translators, improvers, and correctors
- Text summarizers
- Keyword extractors
- Sentiment analyzers
- Social media content generators
- Creative writing assistants
- Specific planner for a complex task
- Text based adventure games

## Why choose Embedia?

- _**Developer friendly**_: Easy to follow documentation, IntelliSense enabled
- _**Pre-defined common AI Agents and Tools**_
- _**LLM agnostic**_: Our universal APIs are LLM independent, it can be used
  with any LLM - whether you're using a service provider like OpenAI, Anthropic,
  Google or have deployed your own open-source model like Llama-2, Falcon, or
  Vicuna.
- _**DB agnostic**_: Our APIs are also independent of what Vector database (or
  Graph Database) you want to connect to your web application. Your vector
  database might be managed by a cloud provider like Weaviate, Pinecone or
  ElasticSearch. Or it might be hosted on a docker container besides your
  webapp.
- _**Pub-sub based event system**_ to build highly customizable workflows
- _**Async**_: Built from ground up to be asynchronus. It works out of the box
  with asynchronomous web frameworks like FastAPI, Starlette, Sanic, etc.
- _**Lightweight**_: Keeping production use-cases in mind, we have kept the
  library's dependencies to a minimum. This makes it a very lightweight
  component in your webstack.
- _**Small dev team**_ with a clear focus on developer experience and
  scalability

## How to use it?

### Step 1: Connect your LLM

```python
import openai
from embedia import ChatLLM


class OpenAIChatLLM(ChatLLM):
    def __init__(self):
        super().__init__()
        openai.api_key = "OPENAI_API_KEY"

    async def _reply(self, prompt):
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            messages=[
                {"role": msg.role, "content": msg.content} for msg in self.chat_history
            ],
        )
        return completion.choices[0].message.content
```

### Step 2: Use your AI Agent

```python
import asyncio
from embedia.agents import ToolUserAgent
from embedia.tools import PythonInterpreterTool, TerminalTool

# Create an AI agent and give it Tools
ai_agent = ToolUserAgent(
    chatllm=OpenAIChatLLM(), tools=[PythonInterpreterTool(), TerminalTool()]
)

# Ask the AI agent to solve a problem for you
question = "Find the number of lines of code in main.py"
asyncio.run(ai_agent(question))
```

## Quick glance over the library internals

The core classes of Embedia are:

- `Tokenizer`: A class that converts text into tokens
- `LLM`: A class that interfaces with a next token generation type large language model (eg: text-davinci-003)
- `ChatLLM`: A class that interfaces with a chat type large language model (eg: gpt-3.5-turbo)
- `Tool`: A class that can convert any python function into a tool that can be used by the Agent
- `EmbeddingModel`: A class that interfaces with the Embedding Model (eg: text-embedding-ada-002)
- `VectorDB`: A class that interfaces with a vector database (eg: Weaviate)

Pre-defined Tools include:

- `PythonInterpreterTool`: A tool that can run python code in the python interpreter
- `TerminalTool`: A tool that can run shell commands in the terminal
- 10+ file operations tools: For reading, writing, copying, moving, deleting files / folders

Pre-defined Agents include:

- `ToolUserAgent`: LLM powered System-1 thinker that can run tools in a loop by reading their docstrings

Helpers include:

- Pub-sub based event system for building highly customizable workflows
- `Persona`: An enum class containing pre-defined system prompts
- `TextDoc`: A class used for dealing with text documents

Learn about them more on our [documentation page](https://embedia-ai.vercel.app/docs)

## How to contribute to the codebase?

This library is under active and rapid development. We'd love your contributions to make it better. To get started, you can check out [contributing.md](./CONTRIBUTING.md)

## License

Copyright - Sudhanshu Passi, 2023 under the the terms of the [Apache 2.0 license](./LICENSE)
