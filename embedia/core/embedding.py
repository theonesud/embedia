from abc import ABC, abstractmethod
from typing import List, Union, Any
import inspect

from embedia.utils.pubsub import publish_event
from embedia.utils.exceptions import DefinitionError


class EmbeddingModel(ABC):
    def __init__(self) -> None:
        self.id = id(self)
        self._check_init()

    def _check_init(self) -> None:
        sig = inspect.signature(self._embed)
        if not len(sig.parameters) == 1:
            raise DefinitionError("_embed must have one argument: input (str / List[Any])")

    async def _check_call(self, input: Union[List[Any], str]) -> None:
        if isinstance(input, str) or isinstance(input, list):
            if not input:
                raise DefinitionError("EmbeddingModel input must not be empty")
        else:
            raise DefinitionError(f"EmbeddingModel input should be a list or string. Got: {type(input)}")

    async def _check_output(self, resp: List[Any]) -> None:
        if not isinstance(resp, list):
            raise DefinitionError(f"_embed output must be a list, got: {type(resp)}")

    @abstractmethod
    async def _embed(self, input: Union[List[Any], str]) -> List[Any]:
        raise NotImplementedError

    async def __call__(self, input: Union[List[Any], str]) -> List[Any]:
        await self._check_call(input)

        publish_event('embedding_start', data={'id': self.id, 'input': input})

        embedding = await self._embed(input)
        await self._check_output(embedding)

        publish_event('embedding_end', data={'id': self.id, 'embedding': embedding})
        return embedding
