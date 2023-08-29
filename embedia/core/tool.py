from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple
from embedia.utils.pubsub import publish_event
from embedia.utils.exceptions import UserDeniedError
from embedia.utils.typechecking import check_num_outputs, check_type, check_not_false, check_args, check_values
from embedia.schema.pubsub import Event


class Tool(ABC):
    def __init__(self, name: str, desc: str, args: Optional[dict] = {}) -> None:
        self.name = name
        self.desc = desc
        self.args = args
        self._check_init()

    def _check_init(self) -> None:
        check_type(self.name, str, self.__init__, 'name')
        check_type(self.desc, str, self.__init__, 'desc')
        check_type(self.args, dict, self.__init__, 'args')
        check_not_false(self.name, "Tool name")
        check_not_false(self.desc, "Tool description")
        for key in self.args.keys():
            check_type(key, str, self.__init__, 'args key')
        for value in self.args.values():
            check_type(value, str, self.__init__, 'args value')
        check_args(self._run, list(self.args.keys()) + ['self'])

    async def _check_output(self, output: Tuple[Any, int]) -> None:
        check_type(output, tuple, self._run, 'output')
        check_num_outputs(output, 2, self._run, '(output, exit_code)')
        check_type(output[1], int, self._run, 'exit_code')
        check_values(output[1], [0, 1], 'exit_code')

    @abstractmethod
    async def _run(self, *args, **kwargs) -> Tuple[Any, int]:
        raise NotImplementedError

    async def __call__(self, *args, **kwargs) -> Tuple[Any, int]:
        publish_event(Event.ToolStart, data={'id': id(self), 'name': self.__class__.__name__,
                                             'args': args, 'kwargs': kwargs})
        output = await self._run(*args, **kwargs)
        await self._check_output(output)
        publish_event(Event.ToolEnd, data={'id': id(self), 'name': self.__class__.__name__,
                                           'output': output})
        return output

    async def human_confirmation(self, details: dict) -> None:
        user_input = input(f"\nTool: {self.__class__.__name__}\nDetails: {details} (y/n): ")
        if user_input.lower() != 'y':
            raise UserDeniedError(f'Tool: {self.__class__.__name__} Details: {details}')
