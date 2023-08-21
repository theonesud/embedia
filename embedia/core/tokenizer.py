from abc import ABC, abstractmethod
from typing import List


class Tokenizer(ABC):
    """Abstract class for tokenizers.

    Methods:
    --------
    - `_tokenize()`: Implement this method to return the tokens of the input.
    - `__call__()`: This method will call the _tokenize() internally.

    Example:
    --------
    ```
    import tiktoken

    class OpenAITokenizer(Tokenizer):
        async def _tokenize(self, text: str) -> List[int]:
            enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
            return enc.encode(text)
    """

    @abstractmethod
    async def _tokenize(self):
        """This function calls the tokenizer with the input

        Use the __call__ method of the Tokenizer object to call this method. Do not call this method directly.

        Arguments:
        ----------
        - `input`: The input to be passed to the tokenizer.

        Returns:
        --------
        - `tokens`: The tokens of the input.
        """
        pass

    async def __call__(self, *args, **kwargs) -> List[int]:
        return await self._tokenize(*args, **kwargs)
