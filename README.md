<p align="center">
  <a href="https://embedia.ai">
    <img src="https://embedia.ai/logo.png" height="64">
    <h3 align="center">Embedia</h3>
  </a>
</p>

<p align="center">
  Amplify your webapp's capabilities with AI
</p>

<p align="center">
  <a href="https://embedia.ai/"><strong>Website</strong></a> ·
  <a href="https://embedia.ai/docs"><strong>Docs</strong></a> ·
  <a href="https://embedia.ai/blog"><strong>Blog</strong></a> ·
  <a href="https://twitter.com/Embedia_ai"><strong>Twitter</strong></a> ·
  <a href="https://discord.gg/aQa53fRdXx"><strong>Discord</strong></a>
</p>
<br/>

### What is Embedia?

Embedia is a framework for building LLM-powered (think: ChatGPT-powered) features that can be added to your webapp.

### Some examples of features you can create with Embedia:

- Chatbots (think: ChatGPT) with a permanent memory that can correlate information across multiple chats or access the internet
- Chatbots with a specific personality (or a combination of personalities)
- Natural language search over a set of documents / webpages / datasets
- Customer support bots with access to the FAQs that can guide the user in the right direction
- Retrieval Augmented Generation (RAG) based recommendation / clustering systems
- AI Agents that work with you to solve problems
- Autonomous AI Agents that can mindfully use the tools you provide
- Entire SAAS products that use LLMs (Opensource or 3rd party) to solve a specific problem

### Why choose Embedia?:

- _**Developer friendly**_: Easy to follow documentation, IntelliSense enabled
- _**Async**_: Built from ground up to be async
- _**Small**_: Has very few dependencies and a tiny package size
- _**Pub-sub based event system**_ to build highly customizable workflows
- _**LLM agnostic**_: Use any LLM you want (ChatGPT, Bard, Llama, Custom-trained, etc)
- _**Vector DB agnostic**_: Use any vector DB you want (Weaviate, Pinecone, Chroma, etc)
- _**Graph DB agnostic**_: Use any graph DB you want (Neo4j, Nebula, etc)
- _**Pre-defined common AI Agents and Tools**_
- _**Small dev team**_ with a clear focus on developer experience and scalability

### How to use it?

- You'll need `Python 3.9` or higher to use this library
- Install using `pip install embedia`

<b>Step 1: Define your Tokenizer class:</b>

```python
import tiktoken
from embedia import Tokenizer

class OpenAITokenizer(Tokenizer):
    async def _tokenize(self, text):
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)
```

<b>Step 2: Define your ChatLLM class:</b>

```python
import openai
from embedia import ChatLLM

class OpenAIChatLLM(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer())
        openai.api_key = "YOUR-API-KEY"

    async def _reply(self):
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{'role': msg.role, 'content': msg.content}
                      for msg in self.chat_history],
        )
        return completion.choices[0].message.content
```

<b>Step 3: Run your AI Agent</b>

```python
import asyncio
from embedia import Persona
from embedia.agents import ToolUser
from embedia.tools import PythonInterpreter

python_coder = OpenAIChatLLM()
asyncio.run(python_coder.set_system_prompt(
    Persona.CodingLanguageExpert.format(language='Python')
))
code = asyncio.run(python_coder(
    'Count number of lines of python code in the current directory'
))
tool_user = ToolUser(chatllm=OpenAIChatLLM(), tools=[PythonInterpreter()])
asyncio.run(tool_user(code))
```

### Quick glance over the library internals

The core classes of Embedia are:

- `Tokenizer`: A class that converts text into tokens
- `LLM`: A class that interfaces with a next token generation type large language model (eg: text-davinci-003)
- `ChatLLM`: A class that interfaces with a chat type large language model (eg: gpt-3.5-turbo)
- `Tool`: A class that can convert any python function into a tool that can be used by the Agent
- `EmbeddingModel`: A class that interfaces with the Embedding Model (eg: text-embedding-ada-002)
- `VectorDB`: A class that interfaces with a vector database (eg: Weaviate)

Pre-defined Tools include:

- `PythonInterpreter`: A tool that can run python code in the python interpreter
- `Terminal`: A tool that can run shell commands in the terminal
- 10+ file operations tools: For reading, writing, copying, moving, deleting files / folders

Pre-defined Agents include:

- `ToolUser`: LLM powered System-1 thinker that can run tools in a loop by reading their docstrings

Helpers include:

- Pub-sub based event system for building highly customizable workflows
- `Persona`: An enum class containing pre-defined system prompts
- `TextDoc`: A class used for dealing with text documents

Learn about them more on their [documentation page](https://embedia.ai/docs)

### How to contribute to the codebase?

This library is under active and rapid development. We'd love your contributions to make it better.

Our goal is to make a developer friendly framework that can help build scalable web applications powered by AI.

To get started, you too can check out the [contributing.md](./CONTRIBUTING.md)

### Become a sponsor

Recurring revenue sponsors will get benefits like:

- Sponsored Screencasts with code
- Early access to Embedia's SAAS products
- Visibility on our website and social media

### Partner with us

We'd love to partner with companies and libraries in the AI and web-dev ecosystem. If you'd like to get in touch, we're always active on our [Discord server](https://discord.gg/aQa53fRdXx).

### License

Copyright - Sudhanshu Passi, 2023 under the the terms of the [Apache 2.0 license](./LICENSE)
