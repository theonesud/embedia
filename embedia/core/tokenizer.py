from abc import ABC, abstractmethod
from typing import List, Any
import inspect
from embedia.utils.exceptions import DefinitionError


class Tokenizer(ABC):
    def __init__(self) -> None:
        self._check_init()

    def _check_init(self) -> None:
        sig = inspect.signature(self._tokenize)
        if not len(sig.parameters) == 1:
            raise DefinitionError("_tokenize must have one argument: text (string)")

    async def _check_call(self, text: str) -> None:
        if not isinstance(text, str):
            raise DefinitionError(f"Tokenizer input must be of type: String, got: {type(text)}")
        if not text:
            raise DefinitionError("Tokenizer input must not be empty")

    async def _check_output(self, tokens: List[Any]) -> None:
        if not isinstance(tokens, list):
            raise DefinitionError(f"_tokenize should return a list, got: {type(tokens)}")

    @abstractmethod
    async def _tokenize(self, text: str) -> List[Any]:
        raise NotImplementedError

    async def __call__(self, text: str) -> List[Any]:
        await self._check_call(text)
        tokens = await self._tokenize(text)
        await self._check_output(tokens)
        return tokens
