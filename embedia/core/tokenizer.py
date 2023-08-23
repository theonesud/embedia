from abc import ABC, abstractmethod
from typing import List
from embedia.utils.exceptions import DefinitionError


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

    def __init__(self):
        pass

    @abstractmethod
    async def _tokenize(self, input: str) -> List[int]:
        """This function calls the tokenizer with the input

        Use the __call__ method of the Tokenizer object to call this method. Do not call this method directly.

        Arguments:
        ----------
        - `input`: The input to be passed to the tokenizer.

        Returns:
        --------
        - `tokens`: The tokens of the input.
        """
        raise NotImplementedError

    async def __call__(self, *args, **kwargs) -> List[int]:
        tokens = await self._tokenize(*args, **kwargs)
        if not isinstance(tokens, list):
            raise DefinitionError(f"Tokenizer output must be a list, got: {type(tokens)}")
        if tokens and not isinstance(tokens[0], int):
            raise DefinitionError(f"Tokenizer output must be a list of integers, got: {type(tokens[0])}")
        return tokens
