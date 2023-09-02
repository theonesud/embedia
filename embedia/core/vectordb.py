from abc import ABC, abstractmethod
from typing import Any, List

from embedia.schema.vectordb import VectorDBGetSimilar, VectorDBInsert


class VectorDB(ABC):
    def __init__(self) -> None:
        pass

    async def insert(self, data: VectorDBInsert) -> None:
        return await self._insert(data)

    async def get_similar(self, data: VectorDBGetSimilar) -> List[Any]:
        return await self._get_similar(data)

    @abstractmethod
    async def _insert(self, data: VectorDBInsert) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _get_similar(self, data: VectorDBGetSimilar) -> List[Any]:
        raise NotImplementedError
