# Tokenizer

`Tokenizer` is an abstract class.
Your `Tokenizer` subclass needs to define the `_tokenize` method.

In the `_tokenize` method you need tokenize the input text into a list of tokens. The tokens can be of any type.

To use your subclass, call the class instance like a function with the input text as the argument.


## Basic Usage

> Remember to add `async` before the definition of `_tokenize` and `await` before calling the subclass instance.

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