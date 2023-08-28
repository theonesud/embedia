from abc import ABC, abstractmethod
from typing import List, Any
import inspect

from embedia.utils.exceptions import DefinitionError


class VectorDB(ABC):
    def __init__(self) -> None:
        self._check_init()

    def _check_init(self) -> None:
        sig = inspect.signature(self._insert)
        if not len(sig.parameters) == 4:
            raise DefinitionError("_insert must have four argument in this order: "
                                  "id: str, text: str, meta: dict, embedding: List[Any]")
        sig = inspect.signature(self._get_similar)
        if not len(sig.parameters) == 2:
            raise DefinitionError("_get_similar must have two argument in this order: "
                                  "embedding: List[Any], n_results: int")

    async def _check_insert(self, id: str, text: str, meta: dict, embedding: List[Any]) -> None:
        if not isinstance(id, str):
            raise DefinitionError(f"VectorDB id must be of type: String, got: {type(id)}")
        if not isinstance(text, str):
            raise DefinitionError(f"VectorDB text must be of type: String, got: {type(text)}")
        if not isinstance(meta, dict):
            raise DefinitionError(f"VectorDB meta must be of type: Dictionary, got: {type(meta)}")
        if not isinstance(embedding, list):
            raise DefinitionError(f"VectorDB embedding must be of type: List[Any], got: {type(embedding)}")
        if not id:
            raise DefinitionError("VectorDB id must not be empty")
        if not text:
            raise DefinitionError("VectorDB text must not be empty")
        if not embedding:
            raise DefinitionError("VectorDB embedding must not be empty")

    async def _check_get_similar(self, embedding: List[Any], n_results: int) -> None:
        if not isinstance(embedding, list):
            raise DefinitionError(f"VectorDB embedding must be of type: List[Any], got: {type(embedding)}")
        if not isinstance(n_results, int):
            raise DefinitionError(f"VectorDB n_results must be of type: Integer, got: {type(n_results)}")
        if n_results < 1:
            raise DefinitionError(f"VectorDB n_results must be greater than 0, got: {n_results}")
        if not embedding:
            raise DefinitionError("VectorDB embedding must not be empty")

    async def _check_output(self, similar: List[Any]) -> None:
        if not isinstance(similar, list):
            raise DefinitionError(f"_get_similar output must be a list, got: {type(similar)}")

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
