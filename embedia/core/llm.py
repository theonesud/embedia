from abc import ABC, abstractmethod
from typing import Optional

from embedia.core.tokenizer import Tokenizer
from embedia.schema.pubsub import Event
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length
# from embedia.utils.typechecking import (check_min_val, check_not_false,
#                                         check_num_args, check_type)


class LLM(ABC):
    def __init__(self, tokenizer: Optional[Tokenizer] = None, max_input_tokens: Optional[int] = None) -> None:
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens
        # self._check_init()

    # def _check_init(self) -> None:
        # check_type(self.tokenizer, Tokenizer, self.__init__, 'tokenizer')
        # check_type(self.max_input_tokens, int, self.__init__, 'max_input_tokens')
        # check_min_val(self.max_input_tokens, 1, 'max_input_tokens')
        # check_num_args(self._complete, 1, "type: str")

    # async def _check_call(self, prompt: str) -> None:
        # check_type(prompt, str, self.__call__)
        # check_not_false(prompt, "LLM __call__ input")

    # async def _check_output(self, completion: str) -> None:
    #     check_type(completion, str, self._complete, 'output')

    @abstractmethod
    async def _complete(self, prompt: str) -> str:
        raise NotImplementedError

    async def __call__(self, prompt: str) -> str:
        # await self._check_call(prompt)

        if self.tokenizer:
            tokens = await self.tokenizer(prompt)
            if self.max_input_tokens:
                check_token_length(len(tokens), self.max_input_tokens)
            num_tokens = len(tokens)
        else:
            num_tokens = None
        publish_event(Event.LLMStart, data={'id': id(self), 'prompt': prompt, 'num_tokens': num_tokens})

        completion = await self._complete(prompt)
        # await self._check_output(completion)

        if self.tokenizer:
            tokens = await self.tokenizer(completion)
            num_tokens = len(tokens)
        else:
            num_tokens = None
        publish_event(Event.LLMEnd, data={'id': id(self), 'completion': completion,
                                          'num_tokens': num_tokens})

        return completion
