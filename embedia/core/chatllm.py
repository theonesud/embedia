import pickle
from abc import ABC
import aiofiles

from embedia.core.llm import LLM
from embedia.core.tokenizer import Tokenizer
from embedia.schema.message import Message, MessageRole
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length
from embedia.utils.typechecking import check_num_args, check_type, check_not_false, check_min_val
from embedia.schema.pubsub import Event


class ChatLLM(ABC):
    def __init__(self, tokenizer: Tokenizer, max_input_tokens: int) -> None:
        self.chat_history = []
        self.llm: LLM = None
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens
        self._check_init()

    def _check_init(self) -> None:
        check_type(self.tokenizer, Tokenizer, self.__init__, 'tokenizer')
        check_type(self.max_input_tokens, int, self.__init__, 'max_input_tokens')
        check_min_val(self.max_input_tokens, 1, 'max_input_tokens')
        check_num_args(self._reply, 1, "type: str")

    async def _check_call(self, prompt: str) -> None:
        check_not_false(self.chat_history, "System Prompt")
        check_type(prompt, str, self.__call__)
        check_not_false(prompt, "ChatLLM __call__ prompt")

    async def _check_output(self, reply: str) -> None:
        check_type(reply, str, self._reply, 'output')

    async def _call_llm(self, message: Message) -> Message:
        prompt = ''
        for message in self.chat_history:
            prompt += "{}: {}\n".format(message.role, message.content)
        prompt += f"{MessageRole.assistant}: "
        reply = await self.llm(prompt)
        return Message(role=MessageRole.assistant, content=reply)

    async def _calculate_chat_history_tokens(self) -> int:
        # Ref: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        total_tokens = 0
        for message in self.chat_history:
            total_tokens += len(await self.tokenizer(message.content))
        return total_tokens

    async def _call_chatllm(self, message: Message) -> Message:
        total_tokens = await self._calculate_chat_history_tokens()
        check_token_length(total_tokens, self.max_input_tokens)
        publish_event(Event.ChatLLMStart, data={'id': id(self), 'role': message.role, 'content': message.content,
                                                'num_tokens': len(await self.tokenizer(message.content))})
        reply = await self._reply(message.content)
        await self._check_output(reply)
        publish_event(Event.ChatLLMEnd, data={'id': id(self), 'role': reply.role, 'content': reply.content,
                                              'num_tokens': len(await self.tokenizer(reply.content))})
        return reply

    async def _reply(self, prompt: str) -> str:
        raise NotImplementedError

    async def __call__(self, prompt: str) -> str:
        await self._check_call(prompt)
        message = Message(role=MessageRole.user, content=prompt)
        self.chat_history.append(message)
        if self.llm:
            reply = await self._call_llm(message)
        else:
            reply = await self._call_chatllm(message)
        self.chat_history.append(reply)
        return reply.content

    @classmethod
    def from_llm(cls, llm: LLM) -> 'ChatLLM':
        instance = cls(llm.tokenizer, llm.max_input_tokens)
        instance.llm = llm
        return instance

    async def set_system_prompt(self, system_prompt: str) -> None:
        tokens = await self.tokenizer(system_prompt)
        publish_event(Event.ChatLLMInit, data={'id': id(self), 'role': MessageRole.system, 'content': system_prompt,
                                               'num_tokens': len(tokens)})
        self.chat_history = [Message(role=MessageRole.system, content=system_prompt)]

    async def save_chat(self, filepath: str) -> None:
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(pickle.dumps(self.chat_history))

    async def load_chat(self, filepath: str) -> None:
        async with aiofiles.open(filepath, "rb") as f:
            self.chat_history = pickle.loads(await f.read())
