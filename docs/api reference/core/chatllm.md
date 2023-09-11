# ChatLLM

`ChatLLM` is an abstract class.
Your `ChatLLM` subclass needs to define the `_reply` method.

> Not to be confused with the `LLM` class. This class is for LLMs that have a chat interface (eg: gpt-3.5-turbo). For LLMs that have a next token generation interface (eg: text-davinci-003), please use the `LLM` class.

> You can convert an instance of a `LLM` subclass into an instance of a `ChatLLM` subclass (more on that below)

In the `_reply` method, you need to get a reply from your LLM by sending the input message to your LLM and returning the reply.


## Message format

Before we move on to the next step, let's understand the `Message` [Pydantic model](https://docs.pydantic.dev/latest/usage/models/). The `Message` model represents a message sent or received by the `ChatLLM` subclass. It has two main attributes: `role` and `content`. The `role` attribute is chosen from the `MessageRole` enum. The `content` attribute is the actual message content.

The other two attributes `created_at` and `id` are automatically assigned when an instance of the `Message` model is created.

`Run in CodeSandbox`

```python
from embedia import Message, MessageRole

print(MessageRole._member_names_)

msg = Message(role=MessageRole.user, content='Hello World')
print(msg)
```

### Output

```
['user', 'assistant', 'system']
role=<MessageRole.user: 'user'> content='Hello World' id='008bedd2-b182-423b-8a9c-1dfb7d78ba7d' created_at='2023-09-07 10:52:25.771221+05:30'
```

## Basic Usage for ChatLLM

The `ChatLLM` class keeps all the `Message` objects sent and received in its `chat_history` attribute. You can access it from anywhere in your subclass using `self.chat_history`.

> Remember to add `async` before the definition of `_reply` and `await` before calling the subclass instance.

> Note that the `prompt` argument is left unused in the below example because OpenAI needs the entire chat history to generate a reply. But you can use the `prompt` argument if you want to do so.

> The `__call__` method of `ChatLLM` will call the `_reply` function with the input prompt if the `_reply` function takes in a argument. If the `_reply` function does not take in a argument, the `__call__` method will call the `_reply` function without any arguments.

`Run in CodeSandbox`

```python
import openai
import asyncio
from embedia import ChatLLM


class OpenAIChatLLM(ChatLLM):
    def __init__(self):
        super().__init__()
        openai.api_key = "YOUR-API-KEY"

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


if __name__ == '__main__':
    chatllm = OpenAIChatLLM()
    reply = asyncio.run(chatllm('What is the capital of France?'))
    print('>>>', reply)
```

### Output

```
[time: 2023-09-07T10:13:07.476314+05:30] [id: 140506295472032] [event: ChatLLM Start]
user (None tokens):
What is the capital of France?

[time: 2023-09-07T10:13:09.257446+05:30] [id: 140506295472032] [event: ChatLLM End]
assistant (None tokens):
The capital of France is Paris.
>>> The capital of France is Paris.
```


## Saving and loading chat_history

You can save and load the `chat_history` variable in a `pickle` file by using the `save_chat` and `load_chat` methods respectively.

> Note that both of them are async functions. So you need to use `await` before calling them. Or you can use `asyncio.run` to run them in the main thread.

`Run in CodeSandbox`

```python
import openai
import os
import asyncio
from embedia import ChatLLM


class OpenAIChatLLM(ChatLLM):
    def __init__(self):
        super().__init__()
        openai.api_key = "YOUR-API-KEY"

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


if __name__ == '__main__':
    chatllm = OpenAIChatLLM()
    reply = asyncio.run(chatllm('What is the capital of France?'))
    reply = asyncio.run(chatllm('What is the capital of Italy?'))
    asyncio.run(chatllm.save_chat('openai_chatllm.pkl'))
    asyncio.run(chatllm.load_chat('openai_chatllm.pkl'))
    assert os.path.exists('openai_chatllm.pkl')
    print(chatllm.chat_history)
```

### Output

```
[time: 2023-09-07T12:04:39.249841+05:30] [id: 140390366465952] [event: ChatLLM Start]
user (None tokens):
What is the capital of France?

[time: 2023-09-07T12:04:40.055116+05:30] [id: 140390366465952] [event: ChatLLM End]
assistant (None tokens):
The capital of France is Paris.

[time: 2023-09-07T12:04:40.113975+05:30] [id: 140390366465952] [event: ChatLLM Start]
user (None tokens):
What is the capital of Italy?

[time: 2023-09-07T12:04:40.981469+05:30] [id: 140390366465952] [event: ChatLLM End]
assistant (None tokens):
The capital of Italy is Rome.
[Message(role=<MessageRole.user: 'user'>, content='What is the capital of France?', id='a1de6077-9eed-4346-9391-66aa0d09efc6', created_at='2023-09-07 12:04:39.249812+05:30'), Message(role=<MessageRole.assistant: 'assistant'>, content='The capital of France is Paris.', id='99633ab0-45ca-481d-9152-ad2ca665dd5d', created_at='2023-09-07 12:04:40.055089+05:30'), Message(role=<MessageRole.user: 'user'>, content='What is the capital of Italy?', id='d1c6ff3a-f1b7-4195-83eb-1c9707cec4cd', created_at='2023-09-07 12:04:40.113947+05:30'), Message(role=<MessageRole.assistant: 'assistant'>, content='The capital of Italy is Rome.', id='f3e1dd9b-6c48-4aa8-b1d8-e642660d6585', created_at='2023-09-07 12:04:40.981338+05:30')]
```

## Personas

Before we move on to the next step, let's understand the `Persona` enum. It contains common system prompts that will define how the LLM responds to your input. Some of these system prompts have placeholders that you'll need to fill in with the appropriate values.

> `Help Needed:` If you want to improve a prompt or add new ones, please open a pull request on GitHub.

`Run in CodeSandbox`

```python
from embedia import Persona

print('1:', Persona.CodingLanguageExpert.format(language='Python'))
print('2:', Persona.LibraryExpert.format(language='JavaScript', library='React'))
print('3:', Persona.Summary.value)
print('4:', Persona.LanguageImprover.format(language='English'))

print(len(Persona._member_names_), Persona._member_names_)
```

### Output

```
1: You are an expert in writing Python code. Only use Python default libraries. Reply only with the code and nothing else
2: You are an expert in writing JavaScript code using React. Reply only with the code and nothing else
3: You are an expert in summarizing a document. Use bullet points to go over all the important points, insights and details in the document. Reply with the summary and nothing else
4: You are an expert in English. I will give you a statement in English, you need convert it from a level A1 to level C2 without changing its meaning. Reply only with the improved statement and nothing else
53 ['Sys1Thinker', 'ArgChooser', 'ToolChooser', 'MetaPrompt', 'MidjourneyPrompt', 'CodingLanguageExpert', 'LibraryExpert', 'CodingLanguageTranslator', 'LibraryTranslator', 'LinuxExpert', 'SQLExpert', 'SVGExpert', 'RegexExpert', 'Documentation', 'TimeComplexity', 'BugFinder', 'CodeImprover', 'ProsCons', 'ProblemBreaker', 'QuestionAsker', 'ProjectManager', 'PRDWriter', 'BackendEngineer', 'FrontendEngineer', 'EssayWriter', 'SocialMediaContent', 'Blogger', 'Summary', 'Simplify', 'KeywordExtractor', 'SubjectExpert', 'JobInterviewer', 'Character', 'Comedian', 'Philosopher', 'Buddha', 'AIPhilosopher', 'LanguageDetector', 'LanguageExpert', 'LanguageTranslator', 'GrammarCorrector', 'LanguageImprover', 'Synonym', 'Antonym', 'Etymologist', 'SentimentAnalyser', 'Storyteller', 'Poet', 'Rapper', 'InteractiveFiction', 'ChessPlayer', 'AsciiArtist', 'LabFlask']
```

## Using ChatLLM with system prompt

You can set the system prompt for the `ChatLLM` subclass by using its `set_system_prompt` method. This erases the `chat_history` and sets the provided system prompt as the first message in the `chat_history`.

> We recommend keeping the LLM temperature low when you ask it to write code.

`Run in CodeSandbox`

```python
import openai
import asyncio
from embedia import ChatLLM, Persona


class OpenAIChatLLM(ChatLLM):
    def __init__(self):
        super().__init__()
        openai.api_key = "YOUR-API-KEY"

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


if __name__ == '__main__':
    chatllm = OpenAIChatLLM()
    asyncio.run(chatllm.set_system_prompt(Persona.CodingLanguageExpert.format(language='Python')))
    reply = asyncio.run(chatllm('Count the number of python code lines in the current folder.'))
```

### Output

```
[time: 2023-09-07T10:15:39.415350+05:30] [id: 140145737432992] [event: ChatLLM Init]
system (None tokens):
You are an expert in writing Python code. Only use Python default libraries. Reply only with the code and nothing else

[time: 2023-09-07T10:15:39.459778+05:30] [id: 140145737432992] [event: ChatLLM Start]
user (None tokens):
Count the number of python code lines in the current folder.

[time: 2023-09-07T10:15:42.460177+05:30] [id: 140145737432992] [event: ChatLLM End]
assistant (None tokens):
import os

count = 0

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            with open(os.path.join(root, file), 'r') as f:
                count += sum(1 for line in f if line.strip())

print(count)
```


## Using ChatLLM with Tokenizer and max_input_tokens

Notice that the number of tokens is `None` in the above-printed log. This is because the `ChatLLM` class doesn't have the optional `tokenizer` parameter in the constructor.
If you add the `tokenizer` argument to the `ChatLLM` constructor, it will count the length of the input, output and system message contents.

Another optional parameter is called `max_input_tokens`. If the length of the entire chat history contents is greater than `max_input_tokens`, the class will raise a `ValueError`.

> Note that the way your tokenizer counts the number of tokens might slightly vary from how a service provider (eg: OpenAI) counts them. They might add a few tokens internally for the service to function properly.

> Note that the `max_input_tokens` will not have any effect if the `tokenizer` argument is not passed to the `ChatLLM` constructor.

`Run in CodeSandbox`

```python
from typing import List
import openai
import asyncio
import tiktoken
from embedia import ChatLLM, Tokenizer, Persona


class OpenAITokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

    async def _tokenize(self, text: str) -> List[int]:
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)


class OpenAIChatLLM(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4096)
        openai.api_key = "YOUR-API-KEY"

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


if __name__ == '__main__':
    chatllm = OpenAIChatLLM()
    asyncio.run(chatllm.set_system_prompt(Persona.CodingLanguageExpert.format(language='Python')))
    reply = asyncio.run(chatllm('Count the number of python code lines in the current folder.'))
```

### Output

```
[time: 2023-09-07T11:15:40.270618+05:30] [id: 139770441525136] [event: ChatLLM Init]
system (23 tokens):
You are an expert in writing Python code. Only use Python default libraries. Reply only with the code and nothing else

[time: 2023-09-07T11:15:40.318945+05:30] [id: 139770441525136] [event: ChatLLM Start]
user (12 tokens):
Count the number of python code lines in the current folder.

[time: 2023-09-07T11:15:44.125530+05:30] [id: 139770441525136] [event: ChatLLM End]
assistant (65 tokens):
import os

count = 0

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file), "r") as f:
                count += sum(1 for line in f if line.strip())

print(count)
```

## Converting LLM to ChatLLM

You can convert an instance of an `LLM` subclass into an instance of a `ChatLLM` subclass using the `from_llm` classmethod present in the `ChatLLM` class. Once you've converted the `LLM` instance, you can use it exactly like a `ChatLLM` instance.

Internally, `Embedia` combines all the messages from the `chat_history` and formats them using the message role and its contents. This entire string is then sent to the `LLM` subclass' `__call__` function. This makes an LLM with a next-token generation interface behave like an LLM with a chat interface.

This is very useful since a lot of LLM service providers (and even open-source models) only provide a next-token generation interface and not a chat interface.

The `tokenizer` and `max_input_tokens` parameters behave the same way as they would if it were an `LLM` subclass. Setting the system prompt is also supported for these kinds of instances.

`Run in CodeSandbox`

```python
from typing import List
import openai
import asyncio
import tiktoken
from embedia import LLM, ChatLLM, Tokenizer, Persona


class OpenAITokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

    async def _tokenize(self, text: str) -> List[int]:
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)

class OpenAILLM(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4000)
        openai.api_key = "YOUR-API-KEY"

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.1,
            max_tokens=500,
        )
        return completion.choices[0].text


if __name__ == '__main__':
    llm = OpenAILLM()
    chatllm = ChatLLM.from_llm(llm)
    asyncio.run(chatllm.set_system_prompt(Persona.CodingLanguageExpert.format(language='Python')))
    reply = asyncio.run(chatllm('Count the number of python code lines in the current folder.'))
```

### Output

```
[time: 2023-09-07T11:54:06.194465+05:30] [id: 139839136970736] [event: ChatLLM Init]
system (23 tokens):
You are an expert in writing Python code. Only use Python default libraries. Reply only with the code and nothing else

[time: 2023-09-07T11:54:06.238965+05:30] [id: 139839155767280] [event: LLM Start]
Prompt (43 tokens):
system: You are an expert in writing Python code. Only use Python default libraries. Reply only with the code and nothing else
user: Count the number of python code lines in the current folder.
assistant:

[time: 2023-09-07T11:54:07.877909+05:30] [id: 139839155767280] [event: LLM End]
Completion (59 tokens):


import os

num_lines = 0

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file)) as f:
                num_lines += len(f.readlines())

print(num_lines)
```
