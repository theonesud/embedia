import pickle
from abc import ABC
from typing import List, Optional

from embedia.core.llm import LLM
from embedia.core.tokenizer import Tokenizer
from embedia.schema.message import Message, MessageRole
from embedia.schema.pubsub import Event
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length
from embedia.utils.typechecking import get_num_params


class ChatLLM(ABC):
    """Abstract class for chat based LLMs (eg: gpt-3.5-turbo).
    For LLMs with a next token generation interface (eg: text-davinci-003), use `LLM`.

    Methods
    -------
    - `_reply` (abstract): Implement this method to generate the reply given a prompt.
    - `__call__` : Internally calls the `_reply` method.
    - `from_llm` (classmethod): Create a `ChatLLM` instance from an `LLM` instance.
    - `set_system_prompt` : Clears the `chat_history` and sets the system prompt as the first message.
    - `save_chat` : Save the chat history to a file.
    - `load_chat` : Load the chat history from a file.

    Attributes
    ----------
    - `chat_history` (List[`Message`]): The chat history.
    - `llm` (`LLM`): The LLM instance (only exists if an instance is created using `from_llm` classmethod)
    - `tokenizer` (`Tokenizer`): Used for counting no. of tokens in the prompt and response.
    - `max_input_tokens` (int): Used for checking if the prompt is too long.
    """

    def __init__(
        self,
        tokenizer: Optional[Tokenizer] = None,
        max_input_tokens: Optional[int] = None,
    ) -> None:
        """Constructor for the `ChatLLM` class.

        Parameters
        ----------
        - `tokenizer` (`Tokenizer`, optional): Used for counting no. of tokens in the prompt and response.
        - `max_input_tokens` (int, optional): Used for checking if the prompt is too long.
        """
        self.chat_history: List[Message] = []
        self.llm: LLM = None
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens

    async def _call_llm(self, message: Message) -> Message:
        prompt = ""
        for message in self.chat_history:
            prompt += "{}: {}\n".format(message.role, message.content)
        prompt += f"{MessageRole.assistant}: "
        reply = await self.llm(prompt)
        return Message(role=MessageRole.assistant, content=reply)

    async def _calculate_chat_history_tokens(self) -> int:
        total_tokens = 0
        for message in self.chat_history:
            total_tokens += len(await self.tokenizer(message.content))
        return total_tokens

    async def _call_chatllm(self, message: Message) -> Message:
        if self.tokenizer:
            total_tokens = await self._calculate_chat_history_tokens()
            if self.max_input_tokens:
                check_token_length(total_tokens, self.max_input_tokens)
            msg_tokens = len(await self.tokenizer(message.content))
        else:
            msg_tokens = None
        publish_event(
            Event.ChatLLMStart,
            id(self),
            {
                "msg_role": message.role,
                "msg_content": message.content,
                "msg_tokens": msg_tokens,
            },
        )

        if not get_num_params(self._reply):
            reply = await self._reply()
        else:
            reply = await self._reply(message.content)
        reply = Message(role=MessageRole.assistant, content=reply)
        if self.tokenizer:
            reply_tokens = len(await self.tokenizer(reply.content))
        else:
            reply_tokens = None
        publish_event(
            Event.ChatLLMEnd,
            id(self),
            {
                "msg_role": message.role,
                "msg_content": message.content,
                "msg_tokens": msg_tokens,
                "reply_role": reply.role,
                "reply_content": reply.content,
                "reply_tokens": reply_tokens,
            },
        )
        return reply

    async def _reply(self, prompt: Optional[str] = None) -> str:
        """Generate the reply given a prompt.
        Do not use this method directly. Use `__call__` instead.

        Parameters
        ----------
        - `prompt` (str, optional): The prompt to generate the reply.

        Returns
        -------
        - `reply` (str): The reply.
        """
        raise NotImplementedError

    async def __call__(self, prompt: str) -> str:
        """Generate the reply given a prompt.

        Parameters
        ----------
        - `prompt` (str): The prompt to generate the reply.

        Returns
        -------
        - `reply` (str): The reply.

        Raises
        ------
        - `ValueError`: If the length of the prompt is greater than `max_input_tokens`.
        """
        try:
            _ = self.chat_history
        except AttributeError as e:
            raise NotImplementedError(
                "Please call `ChatLLM` init method from your subclass init method to initialize the chat history"
            ) from e
        # TODO: add testcase for this
        message = Message(role=MessageRole.user, content=prompt)
        self.chat_history.append(message)
        if self.llm:
            reply = await self._call_llm(message)
        else:
            reply = await self._call_chatllm(message)
        self.chat_history.append(reply)
        return reply.content

    @classmethod
    def from_llm(cls, llm: LLM) -> "ChatLLM":
        """Create a `ChatLLM` instance from an `LLM` instance.

        Parameters
        ----------
        - `llm` (`LLM`): The `LLM` instance.

        Returns
        -------
        - `chatllm` (`ChatLLM`): The `ChatLLM` instance.
        """
        instance = cls(llm.tokenizer, llm.max_input_tokens)
        instance.llm = llm
        return instance

    async def set_system_prompt(self, system_prompt: str) -> None:
        """Clears the `chat_history` and sets the `system_prompt` as the first message.

        Parameters
        ----------
        - `system_prompt` (str): The `system_prompt`.
        """
        if self.tokenizer:
            tokens = await self.tokenizer(system_prompt)
            num_tokens = len(tokens)
        else:
            num_tokens = None
        publish_event(
            Event.ChatLLMInit,
            id(self),
            {
                "system_role": MessageRole.system,
                "system_content": system_prompt,
                "system_tokens": num_tokens,
            },
        )
        self.chat_history = [Message(role=MessageRole.system, content=system_prompt)]

    async def save_chat(self, filepath: str) -> None:
        """Save the `chat_history` to a file.

        Parameters
        ----------
        - `filepath` (str): The path to the file.
        """
        with open(filepath, "wb") as f:
            pickle.dump(self.chat_history, f)

    async def load_chat(self, filepath: str) -> None:
        """Load the `chat_history` from a file.

        Parameters
        ----------
        - `filepath` (str): The path to the file.
        """
        with open(filepath, "rb") as f:
            self.chat_history = pickle.loads(f.read())
