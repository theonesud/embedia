from abc import ABC
from typing import Optional
import pickle

from embedia.core.llm import LLM
from embedia.core.tokenizer import Tokenizer
from embedia.schema.message import Message, MessageRole
from embedia.schema.pubsub import Event
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length
from embedia.utils.typechecking import (get_num_args)


class ChatLLM(ABC):
    def __init__(self, tokenizer: Optional[Tokenizer] = None, max_input_tokens: Optional[int] = None) -> None:
        self.chat_history = []
        self.llm: LLM = None
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens

    async def _call_llm(self, message: Message) -> Message:
        prompt = ''
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
        publish_event(Event.ChatLLMStart, id(self), {'msg_role': message.role,
                                                     'msg_content': message.content,
                                                     'msg_tokens': msg_tokens})

        if not get_num_args(self._reply):
            reply = await self._reply()
        else:
            reply = await self._reply(message.content)
        reply = Message(role=MessageRole.assistant, content=reply)
        if self.tokenizer:
            reply_tokens = len(await self.tokenizer(reply.content))
        else:
            reply_tokens = None
        publish_event(Event.ChatLLMEnd, id(self), {'msg_role': message.role,
                                                   'msg_content': message.content,
                                                   'msg_tokens': msg_tokens,
                                                   'reply_role': reply.role,
                                                   'reply_content': reply.content,
                                                   'reply_tokens': reply_tokens})
        return reply

    async def _reply(self, prompt: Optional[str] = None) -> str:
        raise NotImplementedError

    async def __call__(self, prompt: str) -> str:
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
        if self.tokenizer:
            tokens = await self.tokenizer(system_prompt)
            num_tokens = len(tokens)
        else:
            num_tokens = None
        publish_event(Event.ChatLLMInit, id(self), {'system_role': MessageRole.system,
                                                    'system_content': system_prompt,
                                                    'system_tokens': num_tokens})
        self.chat_history = [Message(role=MessageRole.system, content=system_prompt)]

    async def save_chat(self, filepath: str) -> None:
        with open(filepath, "wb") as f:
            pickle.dump(self.chat_history, f)

    async def load_chat(self, filepath: str) -> None:
        with open(filepath, "rb") as f:
            self.chat_history = pickle.loads(f.read())
