from abc import ABC, abstractmethod


class LLM(ABC):

    @abstractmethod
    async def complete(self):
        pass
