from abc import ABC, abstractmethod
from typing import Optional, Type
from embedia.chatllm import ChatLLM
import logging
import inspect
from embedia.utils.typechecking import enforce_class_type


class DeniedByUserException(Exception):
    pass


class Tool(ABC):

    def __init__(self, name: str, desc: str, examples: str,
                 args: Optional[str] = None, returns: Optional[str] = None,
                 chatllm: Optional[Type[ChatLLM]] = None):
        enforce_class_type(chatllm, ChatLLM)
        self.chatllm = chatllm
        self.args = args
        self.docstring = (f"Name: {name}\n"
                          f"Description: {desc}\n"
                          f"Examples: {examples}\n")
        if args:
            self.docstring += f"Args: {args}\n"
        if returns:
            self.docstring += f"Returns: {returns}\n"

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
                raise ValueError(f"Argument: {arg_name} not found in args docsting: {self.args}")

        logging.info(f"Running {self.__class__.__name__} with args: {args} and kwargs: {kwargs}")
        output = await self._run(*args, **kwargs)
        logging.info(f"Finished running {self.__class__.__name__} with output: {output}")
        return output

    @abstractmethod
    async def _run(self):
        pass
