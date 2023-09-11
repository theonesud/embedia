# Embedding Model

`EmbeddingModel` is an abstract class. Your `EmbeddingModel` subclass needs to define the `_embed` method.

In the `_embed` method, you need to convert the input text into an embedding.

To use your subclass, call the class instance like a function with the input text as the argument.

## Basic Usage

> Remember to add `async` before the definition of `_embed` and `await` before calling the subclass instance.

`Run in CodeSandbox`

```python
import openai
import asyncio
from embedia import EmbeddingModel
from tenacity import (retry, retry_if_not_exception_type, stop_after_attempt,
                      wait_random_exponential)


class OpenAIEmbedding(EmbeddingModel):
    def __init__(self):
        super().__init__()
        openai.api_key = "YOUR-API-KEY"

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
           retry=retry_if_not_exception_type(openai.InvalidRequestError))
    async def _embed(self, input: str):
        result = await openai.Embedding.acreate(input=input, model='text-embedding-ada-002')
        return result["data"][0]["embedding"]


if __name__ == '__main__':
    embedding_model = OpenAIEmbedding()
    embedding = asyncio.run(embedding_model('Hello World'))
```

### Output
```
[time: 2023-09-08T21:29:55.593869+05:30] [id: 140341561335232] [event: Embedding Start]
Input:
Hello World...

[time: 2023-09-08T21:29:56.183640+05:30] [id: 140341561335232] [event: Embedding End]
Embedding:
[-0.007095980923622847, 0.0034716210793703794, -0.007000518962740898, -0.029045790433883667, -0.012976417317986488]...
```
