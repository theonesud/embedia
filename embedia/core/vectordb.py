from abc import ABC, abstractmethod
from typing import Any, List

from embedia.schema.vectordb import VectorDBGetSimilar, VectorDBInsert


class VectorDB(ABC):
    """Abstract class for vector databases.

    Methods
    -------
    - `_insert` (abstract): Implement this method to insert a vector into the database.
    - `_get_similar` (abstract): Implement this method to get similar vectors from the database.
    - `insert` : Internally calls the `_insert` method.
    - `get_similar` : Internally calls the `_get_similar` method.
    """

    def __init__(self) -> None:
        """Constructor for the `VectorDB` class.
        """
        pass

    async def insert(self, data: VectorDBInsert) -> None:
        """Insert a vector/text into the database.

        Parameters
        ----------
        - `data` (`VectorDBInsert`): The vector/text to insert.
        """
        return await self._insert(data)

    async def get_similar(self, data: VectorDBGetSimilar) -> List[Any]:
        """Get similar objects from the database.

        Parameters
        ----------
        - `data` (`VectorDBGetSimilar`): The vector/text to get similar objects for.

        Returns
        -------
        - `similar_objects` (List[Any]): The list of similar objects.
        """
        return await self._get_similar(data)

    @abstractmethod
    async def _insert(self, data: VectorDBInsert) -> None:
        """Insert a vector/text into the database.
        Do not use this method directly. Use `insert` instead.

        Parameters
        ----------
        - `data` (`VectorDBInsert`): The vector/text to insert.
        """
        raise NotImplementedError

    @abstractmethod
    async def _get_similar(self, data: VectorDBGetSimilar) -> List[Any]:
        """Get similar objects from the database.
        Do not use this method directly. Use `get_similar` instead.

        Parameters
        ----------
        - `data` (`VectorDBGetSimilar`): The vector/text to get similar objects for.

        Returns
        -------
        - `similar_objects` (List[Any]): The list of similar objects.
        """
        raise NotImplementedError
