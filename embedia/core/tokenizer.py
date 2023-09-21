from abc import ABC, abstractmethod
from typing import Any, List


class Tokenizer(ABC):
    """Abstract class for tokenizers.

    Methods
    -------
    - `_tokenize` (abstract): Implement this method with the tokenization logic. Do not call this method directly. Instead, call the `__call__` method.
    - `__call__` : Internally calls the `_tokenize` method.
    """

    def __init__(self) -> None:
        """Constructor for the `Tokenizer` class."""
        pass

    @abstractmethod
    async def _tokenize(self, text: str) -> List[Any]:
        """Tokenize a text into a list of tokens.
        Do not use this method directly. Use `__call__` instead.

        Parameters
        ----------
        - `text` (str): The text to tokenize.

        Returns
        -------
        - `tokens` (List[Any]): The list of tokens.
        """
        raise NotImplementedError

    async def __call__(self, text: str) -> List[Any]:
        """Tokenize a text into a list of tokens.

        Parameters
        ----------
        - `text` (str): The text to tokenize.

        Returns
        -------
        - `tokens` (List[Any]): The list of tokens.
        """
        tokens = await self._tokenize(text)
        return tokens
