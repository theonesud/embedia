from abc import ABC, abstractmethod
from typing import Any, List, Union

from embedia.schema.pubsub import Event
from embedia.utils.pubsub import publish_event
# from embedia.utils.typechecking import (check_emb_input, check_num_args,
#                                         check_type)


class EmbeddingModel(ABC):
    def __init__(self) -> None:
        pass
        # self._check_init()

    # def _check_init(self) -> None:
    #     check_num_args(self._embed, 1, "type: str / List[Any]")

    # async def _check_call(self, input: Union[List[Any], str]) -> None:
    #     check_emb_input(input, self.__call__)

    # async def _check_output(self, resp: List[Any]) -> None:
    #     check_type(resp, list, self._embed, 'output')

    @abstractmethod
    async def _embed(self, input: Union[List[Any], str]) -> List[Any]:
        raise NotImplementedError

    async def __call__(self, input: Union[List[Any], str]) -> List[Any]:
        # await self._check_call(input)
        publish_event(Event.EmbeddingStart, data={'id': id(self), 'input': input})
        embedding = await self._embed(input)
        # await self._check_output(embedding)
        publish_event(Event.EmbeddingEnd, data={'id': id(self), 'embedding': embedding})
        return embedding
