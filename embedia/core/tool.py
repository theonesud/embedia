from abc import ABC, abstractmethod
from typing import Union

from embedia.schema.pubsub import Event
from embedia.schema.tool import ToolDocumentation, ToolReturn
from embedia.utils.exceptions import UserDeniedError
from embedia.utils.pubsub import publish_event
from embedia.utils.typechecking import check_params, check_type


class Tool(ABC):
    """Abstract class for tools.

    Methods
    -------
    - `_run` (abstract): Implement this method to run the tool.
    - `__call__` : Internally calls the `_run` method.
    - `human_confirmation` : Ask for human confirmation at any point in the `_run` method.

    Attributes
    ----------
    - `docs` (`ToolDocumentation`): The documentation for the tool.
    """

    def __init__(self, docs: Union[ToolDocumentation, dict]) -> None:
        """Constructor for the `Tool` class.

        Parameters
        ----------
        - `docs` (`ToolDocumentation`/dict): The documentation for the tool.

        Raises
        ------
        - `DefinitionError`: If the `_run` signature does not match the `docs` params.
        """
        if isinstance(docs, dict):
            docs = ToolDocumentation(**docs)
        self.docs = docs
        if self.docs.params:
            check_params(
                self._run, [param.name for param in self.docs.params] + ["self"]
            )

    @abstractmethod
    async def _run(self, *args, **kwargs) -> ToolReturn:
        """Run the tool.
        Do not use this method directly. Use `__call__` instead.

        Parameters
        ----------
        - `*args` : The arguments to the tool.
        - `**kwargs` : The keyword arguments to the tool.

        Returns
        -------
        - `output` (`ToolReturn`/dict): The output of the tool.
        """
        raise NotImplementedError

    async def __call__(self, *args, **kwargs) -> ToolReturn:
        """Run the tool.

        Parameters
        ----------
        - `*args` : The arguments to the tool.
        - `**kwargs` : The keyword arguments to the tool.

        Returns
        -------
        - `output` (`ToolReturn`): The output of the tool.
        """
        try:
            _ = self.docs
        except AttributeError as e:
            raise NotImplementedError(
                "Please call `Tool` init method from your subclass init method with the Tool's documentation"
            ) from e

        publish_event(
            Event.ToolStart,
            id(self),
            {"name": self.__class__.__name__, "args": args, "kwargs": kwargs},
        )
        output = await self._run(*args, **kwargs)
        if isinstance(output, dict):
            output = ToolReturn(**output)
        check_type(output, ToolReturn, self._run, "output")

        publish_event(
            Event.ToolEnd,
            id(self),
            {
                "name": self.__class__.__name__,
                "args": args,
                "kwargs": kwargs,
                "tool_output": output.output,
                "tool_exit_code": output.exit_code,
            },
        )
        return output

    async def human_confirmation(self, details: dict) -> None:
        """Ask for human confirmation at any point in the `_run` method.

        Parameters
        ----------
        - `details` (dict): The details displayed while asking for confirmation.

        Raises
        ------
        - `UserDeniedError`: If the user denies the human confirmation.
        """
        user_input = input(
            f"\nTool: {self.__class__.__name__}\nDetails: {details} Confirm (y/n): "
        )
        if user_input.lower() != "y":
            raise UserDeniedError(f"Tool: {self.__class__.__name__} Details: {details}")
