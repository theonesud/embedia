import inspect
from abc import ABC, abstractmethod

from embedia.core.tokenizer import Tokenizer
from embedia.utils.pubsub import publish_event


class LLM(ABC):
    """Abstract class for next token generation based LLMs.

    For LLMs that have a chatbot like interface, use the ChatbotLLM class.

    Arguments:
    ----------
    - `tokenizer`: An object of the `Tokenizer` class used for counting number of tokens.
    - `max_input_tokens`: The maximum number of tokens allowed in the input message.

    Methods:
    --------
    - `_complete()`: Implement this method to return the completion of your prompt.
    - `__call__()`: This method will call the _complete() internally.

    Example:
    --------
    ```
    class OpenAILLM(LLM):
        async def _complete(self, prompt: str) -> str:
            completion = await openai.Completion.acreate(
                model="text-davinci-003",
                prompt=prompt,
            )
            return completion.choices[0].text

    llm = OpenAILLM()
    print(await llm("The capital of USA is "))

    >>> Washington D.C.
    """

    def __init__(self, tokenizer: Tokenizer, max_input_tokens: int) -> None:
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens
        argspec = inspect.getfullargspec(self._complete)
        arg_names = argspec.args
        if 'prompt' not in arg_names:
            raise ValueError("Argument: prompt not found in _complete definition")
        if set(arg_names) - {'self', 'prompt'}:
            raise ValueError("Only prompt argument is allowed in _complete definition")

    @abstractmethod
    async def _complete(self):
        """This function calls the next token generation based LLM with the prompt
        and returns the completion.

        Use the __call__ method of the LLM object to call this method. Do not call this method directly.

        Arguments:
        ----------
        - `prompt`: The prompt to be passed to the LLM.

        Returns:
        --------
        - `completion`: The completion of the prompt.
        """
        pass

    async def __call__(self, prompt: str) -> str:

        # keep a default log of all chats

        tokens = await self.tokenizer(prompt)
        if len(tokens) > self.max_input_tokens:
            raise ValueError(f"Input text: {len(tokens)} is longer than max_input_tokens: {self.max_input_tokens}")
        publish_event('llm_start', data={'prompt': prompt, 'num_tokens': len(tokens)})
        completion = await self._complete(prompt)
        tokens = await self.tokenizer(completion)
        publish_event('llm_end', data={'completion': completion, 'num_tokens': len(tokens)})
        return completion
