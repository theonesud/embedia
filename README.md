# Embedia
<center> Website: <a href='https://embedia.ai'>embedia.ai</a> </center>
<center> Documentation: <a href='https://embedia.ai/docs'>embedia.ai/docs</a> </center>
<center> Author: <a href='https://twitter.com/Sudhanshupassi'>@sudhanshupassi (twitter)</a> <a href='https://twitter.com/Sudhanshupassi'>@sdhnshu (github)</a> </center>

---
<br>
<i><b>Embedia is what Langchain, Llamaindex and AutoGPT should have been.</b></i>

- It lets you create LLM (think ChatGPT) powered Autonomous AI Agents that are ready for a production release
- We created a universal API interface so you can connect any LLM, Tool, DB to it
- We have an easy to follow [documentation](https://embedia.ai/docs), so you can pick it up fast
- It is natively async and is blazing fast (with sync versions available)
- It has very few dependencies and a tiny package size
- Its transparent - everything action by the LLM is logged
- IntelliSense enabled - your editor will provide suggestions as you type

### Origin story:
As a long time python developer, I've built many backend systems, data processing pipelines and HTTP servers. When ChatGPT took the world by storm, I decided to build applications using LangChain, LlamaIndex, AutoGPT, BabyAGI, etc. But none of them were production ready, their documentations were either non-existent or extremely hard to follow. So I decided to create Embedia - a framework that any developer who wants to build applications using LLMs can use and take them to production.

## How can I use it?
- You'll need `Python 3.9` or higher to use this library
- Installation is a simple command `pip install embedia`

<b>Step 1: Define your ChatLLM class:</b>

```python
from embedia import ChatLLM, Message
import openai

class OpenAILLM(ChatLLM):
    async def reply(self,message: Message) -> Message:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=self.chat_history,
        )
        return Message(**completion.choices[0].message)

```

<b>Step 2: Define your Agent class:</b>

```python
from embedia import Agent
from embedia.tools import PythonREPL

class PythonAgent(Agent):
    llm: OpenAILLM
    tools:[PythonREPL]
```
<b>Step 3: Talk to your Agent</b>

```python
python_agent = PythonAgent()
python_agent.reply("Loop through this folder and list the filenames")
```

```text
>>> Thought: I should write and run python code to loop through this folder and list filenames
>>> Action: import os; [print(f) for f in os.listdir('.') if os.path.isfile(f)]
>>> Observation: file1.py
file2.py
file3.py
```

### Advanced Usage

We provide 3 main classes that you will frequently come across:
- LLM - to communicate with a LLM
- Tool - to run any function you desire
- Agent - runs a loop that uses the LLM to reason, choose parameters for a tool and observe its output

You can use any of our predefined tools, agents or create your own. Just connect them with your LLM and you've created your own Autonomous AI Agent. For details on how to do that, follow the simple steps in our documentation link below

<b><center> Docs: <a href='https://embedia.ai/docs'>embedia.ai/docs</a> </center></b>


## How can I contribute?
If you have a product/service that can be used

we'd love to create convenience functions for them in Embedia. Please check out the [contributing.md](CONTRIBUTING.md).

Or if you simply want to add features, make improvements to Embedia, you too can check out the [contributing.md](CONTRIBUTING.md)

## Support Embedia
If this project helped you, or if you'd like to contribute to an amazing AI project, consider becoming a sponsor.

## License

Copyright Sudhanshu Passi, 2023.

Distributed under the terms of the [Apache 2.0 license](LICENSE), Embedia is free and open source software.