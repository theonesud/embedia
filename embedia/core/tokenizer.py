from abc import ABC, abstractmethod
from typing import Any, List

# from embedia.utils.typechecking import (check_not_false, check_num_args,
#                                         check_type)


class Tokenizer(ABC):
    def __init__(self) -> None:
        pass
        # self._check_init()

    # def _check_init(self) -> None:
    #     check_num_args(self._tokenize, 1, "type: str")

    # async def _check_call(self, text: str) -> None:
    #     check_type(text, str, self.__call__)
    #     check_not_false(text, "Tokenizer __call__ input")

    # async def _check_output(self, tokens: List[Any]) -> None:
    #     check_type(tokens, list, self._tokenize, 'output')

    @abstractmethod
    async def _tokenize(self, text: str) -> List[Any]:
        raise NotImplementedError

    async def __call__(self, text: str) -> List[Any]:
        # await self._check_call(text)
        tokens = await self._tokenize(text)
        # await self._check_output(tokens)
        return tokens
