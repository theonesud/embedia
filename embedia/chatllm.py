from abc import ABC
import pickle
import inspect
from embedia.llm import LLM
from embedia.message import Message


class ChatLLM(ABC):

    def __init__(self, system_prompt: str):
        self.chat_history = [Message(role='system', content=system_prompt)]
        self.llm: LLM = None

    def save_chat(self, filepath: str):
        with open(filepath, 'wb') as f:
            pickle.dump(self.chat_history, f)

    def load_chat(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.chat_history = pickle.load(f)

    async def __call__(self, message: Message) -> Message:
        self.chat_history.append(message)
        if self.llm:
            prompt = ''
            for message in self.chat_history:
                prompt += "{}: {}\n".format(message.role, message.content)
            prompt += "assistant: "
            reply = await self.llm.complete(prompt)
            reply = Message(role='assistant', content=reply)
        else:
            argspec = inspect.getfullargspec(self._reply)
            arg_names = argspec.args
            if 'message' not in arg_names:
                raise ValueError("Argument: message not found in _reply definition")
            if set(arg_names) - {'self', 'message'}:
                raise ValueError("Only message argument is allowed in _reply definition")
            reply = await self._reply(message)
        self.chat_history.append(reply)
        return reply

    @classmethod
    def from_llm(cls, llm: LLM, system_prompt: str):
        instance = cls(system_prompt)
        instance.llm = llm
        return instance

    async def _reply(self, message: Message) -> Message:
        raise NotImplementedError("Please implement _reply method in your ChatLLM subclass")
