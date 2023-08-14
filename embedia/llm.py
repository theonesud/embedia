from abc import ABC, abstractmethod
from embedia.utils.pubsub import publish_event


class LLM(ABC):
    """Abstract class for next token generation based LLMs.

    For LLMs that have a chatbot like interface, use the ChatbotLLM class.

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

    async def __call__(self, *args, **kwargs) -> str:
        publish_event('llm_start', data={'args': args, 'kwargs': kwargs})
        completion = await self._complete(*args, **kwargs)
        publish_event('llm_end', data={'completion': completion})
        return completion
