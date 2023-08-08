from abc import ABC, abstractmethod


class Tokenizer(ABC):

    @abstractmethod
    async def _tokenize(self):
        pass

    async def __call__(self, *args, **kwargs):
        return await self._tokenize(*args, **kwargs)
