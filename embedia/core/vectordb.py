from abc import ABC, abstractmethod
from typing import List

from embedia.core.embedding import EmbeddingModel
from embedia.schema.textdoc import TextDoc
from embedia.utils.exceptions import DefinitionError


class VectorDB(ABC):
    """Abstract class for vector databases.

    Methods:
    --------
    - `_save_embedding()`: Implement this method to save the embedding to the db.
    - `_similarity_search()`: Implement this method to return the most similar embeddings to the query.
    - `save_embedding()`: This method will call the _save_embedding() internally.
    - `similarity_search()`: This method will call the _similarity_search() internally.
    """

    def __init__(self, embedding_model: EmbeddingModel, print=False, log=False) -> None:
        self.embedding_model = embedding_model

    async def insert(self, docs: List[TextDoc]) -> None:
        for doc in docs:
            embedding = await self.embedding_model(doc)
            # TODO: check if _insert can take all 4 params with same var names
            # TODO: make embedding creation optional (if is handled by the db)
            await self._insert(embedding=embedding, meta=doc.meta, text=doc.contents, id=doc.id)

    async def get_similar(self, query: str, n_results: int) -> List[TextDoc]:
        embedding = await self.embedding_model(query)
        # TODO: check if _get_similar can take all 2 params with same var names
        resp = await self._get_similar(embedding=embedding, n_results=n_results)

        if not isinstance(resp, list):
            raise DefinitionError(f"_get_similar output must be a list, got: {type(resp)}")
        if resp and not isinstance(resp[0], TextDoc):
            raise DefinitionError(f"_get_similar output must be a list of TextDoc, got: {type(resp[0])}")

        return resp

    @abstractmethod
    async def _insert(self, embedding: List[float], meta: dict, text: str, id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _get_similar(self, embedding: List[float], n_results: int) -> List[TextDoc]:
        raise NotImplementedError
