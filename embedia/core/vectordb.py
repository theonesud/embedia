from abc import ABC, abstractmethod
from typing import List

from embedia.core.embedding import EmbeddingModel
from embedia.schema.textdoc import TextDoc


class VectorDB(ABC):
    """Abstract class for vector databases.

    Methods:
    --------
    - `_save_embedding()`: Implement this method to save the embedding to the db.
    - `_similarity_search()`: Implement this method to return the most similar embeddings to the query.
    - `save_embedding()`: This method will call the _save_embedding() internally.
    - `similarity_search()`: This method will call the _similarity_search() internally.
    """

    def __init__(self, embedding_model: EmbeddingModel) -> None:
        self.embedding_model = embedding_model

    async def insert(self, docs: List[TextDoc]) -> None:
        for doc in docs:
            embedding = await self.embedding_model(doc)
            await self._insert(embedding)

    async def get_similar(self, query: str):
        embedding = await self.embedding_model(query)
        return await self._get_similar(embedding)

    @abstractmethod
    async def _insert(self):
        pass

    @abstractmethod
    async def _get_similar(self):
        pass
