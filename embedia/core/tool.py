from abc import ABC, abstractmethod

from embedia.schema.pubsub import Event
from embedia.schema.tool import ToolDocumentation, ToolReturn
from embedia.utils.exceptions import UserDeniedError
from embedia.utils.pubsub import publish_event
from embedia.utils.typechecking import (check_args, check_type)


class Tool(ABC):
    def __init__(self, docs: ToolDocumentation) -> None:
        if isinstance(docs, dict):
            docs = ToolDocumentation(**docs)
        self.docs = docs
        if self.docs.args:
            check_args(self._run, [arg.name for arg in self.docs.args] + ['self'])

    @abstractmethod
    async def _run(self, *args, **kwargs) -> ToolReturn:
        raise NotImplementedError

    async def __call__(self, *args, **kwargs) -> ToolReturn:
        publish_event(Event.ToolStart, id(self), {'name': self.__class__.__name__,
                                                  'args': args, 'kwargs': kwargs})
        output = await self._run(*args, **kwargs)
        if isinstance(output, dict):
            output = ToolReturn(**output)
        check_type(output, ToolReturn, self._run, 'output')

        publish_event(Event.ToolEnd, id(self), {'name': self.__class__.__name__,
                                                'args': args, 'kwargs': kwargs,
                                                'output': output})
        return output

    async def human_confirmation(self, details: dict) -> None:
        user_input = input(f"\nTool: {self.__class__.__name__}\nDetails: {details} (y/n): ")
        if user_input.lower() != 'y':
            raise UserDeniedError(f'Tool: {self.__class__.__name__} Details: {details}')
