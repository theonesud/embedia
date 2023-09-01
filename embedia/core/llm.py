from abc import ABC, abstractmethod
from typing import Optional

from embedia.core.tokenizer import Tokenizer
from embedia.schema.pubsub import Event
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length


class LLM(ABC):
    def __init__(self, tokenizer: Optional[Tokenizer] = None,
                 max_input_tokens: Optional[int] = None) -> None:
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens

    @abstractmethod
    async def _complete(self, prompt: str) -> str:
        raise NotImplementedError

    async def __call__(self, prompt: str) -> str:

        if self.tokenizer:
            tokens = await self.tokenizer(prompt)
            if self.max_input_tokens:
                check_token_length(len(tokens), self.max_input_tokens)
            prompt_tokens = len(tokens)
        else:
            prompt_tokens = None
        publish_event(Event.LLMStart, id(self), {'prompt': prompt,
                                                 'prompt_tokens': prompt_tokens})

        completion = await self._complete(prompt)

        if self.tokenizer:
            tokens = await self.tokenizer(completion)
            comp_tokens = len(tokens)
        else:
            comp_tokens = None
        publish_event(Event.LLMEnd, id(self), {'prompt': prompt,
                                               'prompt_tokens': prompt_tokens,
                                               'completion': completion,
                                               'completion_tokens': comp_tokens})

        return completion
