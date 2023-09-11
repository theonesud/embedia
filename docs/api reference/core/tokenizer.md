# Tokenizer

A tokenizer is used to convert a string into a list of tokens. Tokens can either be of type `int` or `str`. To learn more about tokenization, please refer to this [article](https://huggingface.co/docs/transformers/tokenizer_summary).

`Tokenizer` is an abstract class. Inherit from this class and define the `_tokenize` method. To use it, call the class instance like a function with the input text as the argument.

### Methods:
- `_tokenize` (abstract): Implement this method with the tokenization logic. Do not call this method directly. Instead, use the `__call__` method.
    - Expected input: `str`
    - Expected output: `List[Any]`

- `__call__` : Internally calls the `_tokenize` method. Use this method by calling the class instance like a function with the input text as the argument.
    - Expected input: `str`
    - Expected output: `List[int]` or `List[str]`


## Basic Usage

Let's build a tokenizer that OpenAI uses for `gpt-3.5 turbo`, `text-davinci-003` and `gpt-4`. They recommend using the `tiktoken` library for tokenization.

`Run in CodeSandbox`

```python
import asyncio
from typing import List
import tiktoken
from embedia import Tokenizer


class OpenAITokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

    async def _tokenize(self, text: str) -> List[int]:
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)


if __name__ == '__main__':
    tokenizer = OpenAITokenizer()
    tokens = asyncio.run(tokenizer('Lorem ipsum dolor sit amet, consectetur adipiscing elit.'))
    print(tokens)
```

### Output

```
[33883, 27439, 24578, 2503, 28311, 11, 36240, 59024, 31160, 13]
```