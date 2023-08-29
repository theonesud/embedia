from abc import ABC, abstractmethod
from typing import List, Any

from embedia.utils.typechecking import check_num_args, check_type, check_not_false, check_min_val


class VectorDB(ABC):
    def __init__(self) -> None:
        self._check_init()

    def _check_init(self) -> None:
        check_num_args(self._insert, 4, "In order - id: str, text: str, meta: dict, embedding: List[Any]")
        check_num_args(self._get_similar, 2, "In order - embedding: List[Any], n_results: int")

    async def _check_insert(self, id: str, text: str, meta: dict, embedding: List[Any]) -> None:
        check_type(id, str, self._insert, 'id')
        check_type(text, str, self._insert, 'text')
        check_type(meta, dict, self._insert, 'meta')
        check_type(embedding, list, self._insert, 'embedding')
        check_not_false(id, "VectorDB id")
        check_not_false(text, "VectorDB text")
        check_not_false(embedding, "VectorDB embedding")

    async def _check_get_similar(self, embedding: List[Any], n_results: int) -> None:
        check_type(embedding, list, self._get_similar, 'embedding')
        check_type(n_results, int, self._get_similar, 'n_results')
        check_not_false(embedding, "VectorDB embedding")
        check_min_val(n_results, 1, 'VectorDB n_results')

    async def _check_output(self, similar: List[Any]) -> None:
        check_type(similar, list, self._get_similar, 'output')

    async def insert(self, id: str, text: str, meta: dict, embedding: List[Any]) -> None:
        await self._check_insert(id, text, meta, embedding)
        return await self._insert(id, text, meta, embedding)

    async def get_similar(self, embedding: List[Any], n_results: int) -> List[Any]:
        await self._check_get_similar(embedding, n_results)
        similar = await self._get_similar(embedding, n_results)
        await self._check_output(similar)
        return similar

    @abstractmethod
    async def _insert(self, id: str, text: str, meta: dict, embedding: List[Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _get_similar(self, embedding: List[Any], n_results: int) -> List[Any]:
        raise NotImplementedError
