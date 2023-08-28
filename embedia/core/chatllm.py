import pickle
from abc import ABC
import inspect
import aiofiles

from embedia.core.llm import LLM
from embedia.core.tokenizer import Tokenizer
from embedia.schema.message import Message
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length
from embedia.utils.exceptions import DefinitionError


class ChatLLM(ABC):
    def __init__(self, tokenizer: Tokenizer, max_input_tokens: int) -> None:
        self.chat_history = []
        self.llm: LLM = None
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
        sig = inspect.signature(self._reply)
        if not len(sig.parameters) == 1:
            raise DefinitionError("_reply must have one argument: message (Message)")

    async def _check_call(self, message: Message) -> None:
        if not self.chat_history:
            raise DefinitionError("Please set the system prompt using the set_system_prompt method")
        if not isinstance(message, Message):
            raise DefinitionError(f"ChatLLM input must be of type: Message, got: {type(message)}")
        if not message.content:
            raise DefinitionError("ChatLLM Message contents must not be empty")

    async def _check_output(self, reply: Message) -> None:
        if not isinstance(reply, Message):
            raise DefinitionError(f"_reply must return a Message, got: {type(reply)}")

    async def _call_llm(self, message: Message) -> Message:
        prompt = ''
        for message in self.chat_history:
            prompt += "{}: {}\n".format(message.role, message.content)
        prompt += "assistant: "
        reply = await self.llm(prompt)
        reply = Message(role='assistant', content=reply)
        return reply

    async def _calculate_chat_history_tokens(self) -> int:
        # Ref: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        total_tokens = 0
        for message in self.chat_history:
            total_tokens += len(await self.tokenizer(message.content)) + 3
        return total_tokens + 3

    async def _call_chatllm(self, message: Message) -> Message:
        total_tokens = await self._calculate_chat_history_tokens()
        check_token_length(total_tokens, self.max_input_tokens)
        publish_event('chatllm_start', data={'id': self.id, 'role': message.role, 'content': message.content,
                                             'num_tokens': 3 + len(await self.tokenizer(message.content))})

        reply = await self._reply(message)

        await self._check_output(reply)

        tokens = await self.tokenizer(reply.content)
        publish_event('chatllm_end', data={'id': self.id, 'role': reply.role, 'content': reply.content,
                                           'num_tokens': 3 + len(tokens)})

        return reply

    async def _reply(self, message: Message) -> Message:
        raise NotImplementedError

    async def __call__(self, message: Message) -> Message:
        await self._check_call(message)

        self.chat_history.append(message)
        if self.llm:
            reply = await self._call_llm(message)
        else:
            reply = await self._call_chatllm(message)
        self.chat_history.append(reply)

        return reply

    @classmethod
    def from_llm(cls, llm: LLM) -> 'ChatLLM':
        instance = cls(llm.tokenizer, llm.max_input_tokens)
        instance.llm = llm
        return instance

    async def set_system_prompt(self, system_prompt: str) -> None:
        tokens = await self.tokenizer(system_prompt)
        publish_event('chatllm_init', data={'id': self.id, 'role': 'system', 'content': system_prompt,
                                            'num_tokens': 3 + len(tokens)})
        self.chat_history = [Message(role='system', content=system_prompt)]

    async def save_chat(self, filepath: str) -> None:
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(pickle.dumps(self.chat_history))

    async def load_chat(self, filepath: str) -> None:
        async with aiofiles.open(filepath, "rb") as f:
            self.chat_history = pickle.loads(await f.read())
