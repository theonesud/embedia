from abc import ABC, abstractmethod
from typing import List


class Tokenizer(ABC):

    @abstractmethod
    async def _tokenize(self):
        pass

    async def __call__(self, *args, **kwargs) -> List[int]:
        return await self._tokenize(*args, **kwargs)
