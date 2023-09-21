from abc import ABC, abstractmethod
from typing import Any, List, Union

from embedia.schema.pubsub import Event
from embedia.utils.pubsub import publish_event


class EmbeddingModel(ABC):
    """Abstract class for embedding models.

    Methods
    -------
    - `_embed` (abstract): Implement this method to embed a text into a vector.
    - `__call__` : Internally calls the `_embed` method.
    """

    def __init__(self) -> None:
        """Constructor for the `EmbeddingModel` class."""
        pass

    @abstractmethod
    async def _embed(self, input: Union[List[Any], str]) -> List[Any]:
        """Embed a text/token_list into a vector.
        Do not use this method directly. Use `__call__` instead.

        Parameters
        ----------
        - `input` (Union[List[Any], str]): The text/token_list to embed.

        Returns
        -------
        - `embedding` (List[Any]): The embedding of the input.
        """
        raise NotImplementedError

    async def __call__(self, input: Union[List[Any], str]) -> List[Any]:
        """Embed a text/token_list into a vector.

        Parameters
        ----------
        - `input` (Union[List[Any], str]): The text/token_list to embed.

        Returns
        -------
        - `embedding` (List[Any]): The embedding of the input.
        """
        publish_event(Event.EmbeddingStart, id(self), {"input": input})
        embedding = await self._embed(input)
        publish_event(
            Event.EmbeddingEnd, id(self), {"input": input, "embedding": embedding}
        )
        return embedding
