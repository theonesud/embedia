from abc import ABC, abstractmethod
from typing import Optional, Type
from embedia.chatllm import ChatLLM
import logging
import inspect
from embedia.utils.typechecking import enforce_class_type


class DeniedByUserException(Exception):
    pass


class Tool(ABC):

    def __init__(self, name: str, desc: str,
                 args: Optional[str] = None,
                 chatllm: Optional[Type[ChatLLM]] = None):
        enforce_class_type(chatllm, ChatLLM)
        self.chatllm = chatllm
        self.name = name
        self.desc = desc
        self.args = args

    def confirm_before_running(self, *args, **kwargs):
        run_function = input(
            f"Run {self.__class__.__name__} with args: {args} and kwargs: {kwargs} (y/n): ")
        if run_function.lower() != 'y':
            raise DeniedByUserException(
                f'User denied running function: {self.__class__.__name__} with args: {args} '
                f'and kwargs: {kwargs}')

    async def __call__(self, *args, **kwargs):
        argspec = inspect.getfullargspec(self._run)
        arg_names = argspec.args
        for arg_name in arg_names:
            if arg_name == 'self':
                continue
            if arg_name not in self.args:
                # TODO: Do better checking of args docs as per agent.py
                raise ValueError(f"Argument: {arg_name} not found in args docsting: {self.args}")

        logging.info(f"Running {self.__class__.__name__} with args: {args} and kwargs: {kwargs}")
        output = await self._run(*args, **kwargs)
        # TODO: Restrict to one output str variable
        logging.info(f"Finished running {self.__class__.__name__} with output: {output}")
        return output

    @abstractmethod
    async def _run(self):
        pass
