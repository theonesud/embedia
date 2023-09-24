from abc import ABC, abstractmethod
from typing import Optional

from embedia.core.tokenizer import Tokenizer
from embedia.schema.pubsub import Event
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length


class LLM(ABC):
    """Abstract class for next token generation based LLMs (eg: text-davinci-003).
    For LLMs with a chat interface (eg: gpt-3.5-turbo), use `ChatLLM`.

    Methods
    -------
    - `_complete` (abstract): Implement this method to generate the next token(s) given a prompt.
    - `__call__` : Internally calls the `_complete` method.

    Attributes
    ----------
    - `tokenizer` (`Tokenizer`): Used for counting no. of tokens in the prompt and response.
    - `max_input_tokens` (int): Used for checking if the prompt is too long.
    """

    def __init__(
        self,
        tokenizer: Optional[Tokenizer] = None,
        max_input_tokens: Optional[int] = None,
    ) -> None:
        """Constructor for the `LLM` class.

        Parameters
        ----------
        - `tokenizer` (Tokenizer, optional): Used for counting no. of tokens in the prompt and response.
        - `max_input_tokens` (int, optional): Used for checking if the prompt is too long.
        """
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens

    @abstractmethod
    async def _complete(self, prompt: str) -> str:
        """Generate the next token(s) given a prompt.
        Do not use this method directly. Use `__call__` instead.

        Parameters
        ----------
        - `prompt` (str): The prompt to generate the next token(s).

        Returns
        -------
        - `completion` (str): The next token(s).
        """
        raise NotImplementedError

    async def __call__(self, prompt: str) -> str:
        """Generate the next token(s) given a prompt.

        Parameters
        ----------
        - `prompt` (str): The prompt to generate the next token(s).

        Returns
        -------
        - `completion` (str): The next token(s).

        Raises
        ------
        - `ValueError`: If `tokenizer` and `max_input_tokens` exist and length of prompt is greater than `max_input_tokens`.
        """
        if self.tokenizer:
            tokens = await self.tokenizer(prompt)
            if self.max_input_tokens:
                check_token_length(len(tokens), self.max_input_tokens)
            prompt_tokens = len(tokens)
        else:
            prompt_tokens = None
        publish_event(
            Event.LLMStart, id(self), {"prompt": prompt, "prompt_tokens": prompt_tokens}
        )

        completion = await self._complete(prompt)

        if self.tokenizer:
            tokens = await self.tokenizer(completion)
            comp_tokens = len(tokens)
        else:
            comp_tokens = None
        publish_event(
            Event.LLMEnd,
            id(self),
            {
                "prompt": prompt,
                "prompt_tokens": prompt_tokens,
                "completion": completion,
                "completion_tokens": comp_tokens,
            },
        )

        return completion
