import inspect
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple
from embedia.utils.pubsub import publish_event
from embedia.utils.exceptions import DeniedByUserError, DefinitionError


class Tool(ABC):
    def __init__(self, name: str, desc: str, args: Optional[dict] = {}) -> None:
        self.name = name
        self.desc = desc
        self.args = args
        self.id = id(self)
        self._check_init()

    def _check_init(self) -> None:
        if not isinstance(self.name, str):
            raise DefinitionError(f"Tool name must be of type: String, got: {type(self.name)}")
        if not isinstance(self.desc, str):
            raise DefinitionError(f"Tool description must be of type: String, got: {type(self.desc)}")
        if not isinstance(self.args, dict):
            raise DefinitionError(f"Tool args must be of type: Dictionary, got: {type(self.args)}")
        if not all(isinstance(key, str) for key in self.args.keys()):
            raise DefinitionError("Tool args keys must be of type: String")
        if not all(isinstance(value, str) for value in self.args.values()):
            raise DefinitionError("Tool args values must be of type: String")
        if not self.name:
            raise DefinitionError("Tool name must not be empty")
        if not self.desc:
            raise DefinitionError("Tool description must not be empty")
        args = list(self.args.keys()) + ['self']
        argspec = inspect.getfullargspec(self._run)
        arg_names = argspec.args
        if set(arg_names) != set(args):
            raise DefinitionError(f"{self._run.__qualname__} expects arguments: {set(args)},"
                                  f" got: {set(arg_names)}")

    async def _check_output(self, output: Tuple[Any, int]) -> None:
        if not isinstance(output, tuple):
            raise DefinitionError(f"_run output must be a tuple like (output, exit_code),"
                                  f" got: {type(output)}")
        if not len(output) == 2:
            raise DefinitionError(f"_run output must be a tuple like (output, exit_code),"
                                  f" got: {output}")
        if output[1] not in [0, 1]:
            raise DefinitionError(f"_run exit code must be 0 or 1, got: {output[1]}")

    @abstractmethod
    async def _run(self, *args, **kwargs) -> Tuple[Any, int]:
        raise NotImplementedError

    async def __call__(self, *args, **kwargs) -> Tuple[Any, int]:
        publish_event('tool_start', data={'id': self.id, 'name': self.__class__.__name__,
                                          'args': args, 'kwargs': kwargs})
        # TODO: add Esc keyboard interrupt to stop the _run function
        # TODO: add a helper func to run tool in a separate thread/process
        output = await self._run(*args, **kwargs)
        await self._check_output(output)
        publish_event('tool_end', data={'id': self.id, 'name': self.__class__.__name__,
                                        'output': output})
        return output

    def human_confirmation(self, details: dict) -> None:
        user_input = input(f"\nTool: {self.__class__.__name__}\nDetails: {details} (y/n): ")
        if user_input.lower() != 'y':
            raise DeniedByUserError(f'Tool: {self.__class__.__name__}\nDetails: {details}')
