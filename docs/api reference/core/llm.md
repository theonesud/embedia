# LLM

`LLM` is an abstract class.
Your `LLM` subclass needs to define the `_complete` method.

> Not to be confused with the `ChatLLM` class. This class is for LLMs that have a next token generation interface (eg: text-davinci-003). For LLMs that have a chat interface (eg: gpt-3.5-turbo), please use the `ChatLLM` class.

> You can convert an instance of a `LLM` subclass into an instance of a `ChatLLM` subclass (please check `ChatLLM` documentation for more details)

In the `_complete` method, you need to generate a text completion by sending the input prompt to your LLM and return the completion.

To use your subclass, call the class instance like a function with the input prompt as the argument.


## Basic Usage

> Remember to add `async` before the definition of `_complete` and `await` before calling the subclass instance.

`Run in CodeSandbox`

```python
import asyncio
import openai
from embedia import LLM


class OpenAILLM(LLM):
    def __init__(self):
        super().__init__()
        openai.api_key = "YOUR-API-KEY"

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt
        )
        return completion.choices[0].text


if __name__ == '__main__':
    llm = OpenAILLM()
    completion = asyncio.run(llm('The capital of France is '))
    print('>>>', completion)
```

### Output

```
[time: 2023-09-06T11:06:05.118292+05:30] [id: 140454427147664] [event: LLM Start]
Prompt (None tokens):
The capital of France is

[time: 2023-09-06T11:06:05.768938+05:30] [id: 140454427147664] [event: LLM End]
Completion (None tokens):

Paris.
>>>  Paris.
```


## Usage with Tokenizer

Notice that the number of tokens is `None` in the above-printed log. This is because the `LLM` class doesn't have the optional `tokenizer` parameter in the constructor.
If you add the `tokenizer` argument to the `LLM` constructor, it will count the length of the input and output in tokens.

> Note that the way your tokenizer counts the number of tokens might slightly vary from how a service provider (eg: OpenAI) counts them. They might add a few tokens internally for the service to function properly.

`Run in CodeSandbox`

```python
import openai
import asyncio
from typing import List
import tiktoken
from embedia import LLM, Tokenizer


class OpenAITokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

    async def _tokenize(self, text: str) -> List[int]:
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)


class OpenAILLM(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer())
        openai.api_key = "YOUR-API-KEY"

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt
        )
        return completion.choices[0].text


if __name__ == '__main__':
    llm = OpenAILLM()
    completion = asyncio.run(llm('The capital of France is '))
    print('>>>', completion)
```

### Output

```
[time: 2023-09-06T18:29:14.426081+05:30] [id: 140207913138976] [event: LLM Start]
Prompt (6 tokens):
The capital of France is

[time: 2023-09-06T18:29:14.910721+05:30] [id: 140207913138976] [event: LLM End]
Completion (3 tokens):

Paris.
>>>  Paris.
```


## Usage with Tokenizer and max_input_tokens

There's also another optional parameter in the `LLM` constructor called `max_input_tokens`. If the length of the input prompt is greater than `max_input_tokens`, the class will raise a `ValueError`.

> Note that the `max_input_tokens` will not have any effect if the `tokenizer` argument is not passed to the `LLM` constructor.

`Run in CodeSandbox`

```python
import openai
import asyncio
from typing import List
import tiktoken
from embedia import LLM, Tokenizer


class OpenAITokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

    async def _tokenize(self, text: str) -> List[int]:
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)


class OpenAILLM(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=2)
        openai.api_key = "YOUR-API-KEY"

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt
        )
        return completion.choices[0].text


if __name__ == '__main__':
    llm = OpenAILLM()
    completion = asyncio.run(llm('The capital of France is '))
    print('>>>', completion)
```

### Output

```
ValueError: Length of input text: 6 token(s) is longer than max_input_tokens: 2
```
