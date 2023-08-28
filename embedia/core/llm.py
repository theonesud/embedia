from abc import ABC, abstractmethod
import inspect

from embedia.core.tokenizer import Tokenizer
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length
from embedia.utils.exceptions import DefinitionError


class LLM(ABC):
    def __init__(self, tokenizer: Tokenizer, max_input_tokens: int) -> None:
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens
        self.id = id(self)
        self._check_init()

    def _check_init(self) -> None:
        if not isinstance(self.tokenizer, Tokenizer):
            raise DefinitionError(f"Tokenizer must be of type: Tokenizer, got: {type(self.tokenizer)}")
        if not isinstance(self.max_input_tokens, int):
            raise DefinitionError(f"Max input tokens must be of type: Integer, got: {type(self.max_input_tokens)}")
        if self.max_input_tokens < 1:
            raise DefinitionError(f"Max input tokens must be greater than 0, got: {self.max_input_tokens}")
        sig = inspect.signature(self._complete)
        if not len(sig.parameters) == 1:
            raise DefinitionError("_complete must have one argument: prompt (string)")

    async def _check_call(self, prompt: str) -> None:
        if not isinstance(prompt, str):
            raise DefinitionError(f"LLM input must be of type: String, got: {type(prompt)}")
        if not prompt:
            raise DefinitionError("LLM input must not be empty")

    async def _check_output(self, completion: str) -> None:
        if not isinstance(completion, str):
            raise DefinitionError(f"_complete should return a string, got: {type(completion)}")

    @abstractmethod
    async def _complete(self, prompt: str) -> str:
        raise NotImplementedError

    async def __call__(self, prompt: str) -> str:
        await self._check_call(prompt)

        tokens = await self.tokenizer(prompt)
        check_token_length(len(tokens), self.max_input_tokens)
        publish_event('llm_start', data={'id': self.id, 'prompt': prompt, 'num_tokens': 3 + len(tokens)})

        completion = await self._complete(prompt)
        await self._check_output(completion)

        tokens = await self.tokenizer(completion)
        publish_event('llm_end', data={'id': self.id, 'completion': completion,
                                       'num_tokens': 3 + len(tokens)})

        return completion
