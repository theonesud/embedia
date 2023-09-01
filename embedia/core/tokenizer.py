from abc import ABC, abstractmethod
from typing import Any, List


class Tokenizer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def _tokenize(self, text: str) -> List[Any]:
        raise NotImplementedError

    async def __call__(self, text: str) -> List[Any]:
        tokens = await self._tokenize(text)
        return tokens
