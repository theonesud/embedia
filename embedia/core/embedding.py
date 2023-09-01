from abc import ABC, abstractmethod
from typing import Any, List, Union

from embedia.schema.pubsub import Event
from embedia.utils.pubsub import publish_event


class EmbeddingModel(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def _embed(self, input: Union[List[Any], str]) -> List[Any]:
        raise NotImplementedError

    async def __call__(self, input: Union[List[Any], str]) -> List[Any]:
        publish_event(Event.EmbeddingStart, id(self), {'input': input})
        embedding = await self._embed(input)
        publish_event(Event.EmbeddingEnd, id(self), {'input': input,
                                                     'embedding': embedding})
        return embedding
