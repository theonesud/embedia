import inspect
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple
from embedia.utils.pubsub import publish_event
from embedia.utils.exceptions import DeniedByUserException, DefinitionError


class Tool(ABC):
    """Abstract class for a tool.

    Arguments:
    ----------
    - `name`: The name of the tool.
    - `desc`: The description of the tool.
    - `args`: The arguments of the tool. It is a dictionary with the keys as the argument names
        and the values as the argument descriptions.
    - `chatllm`: (Optional) The chatllm class to be used for the tool.

    Methods:
    --------
    - `_run()`: Implement this method to run the tool and return the output of the tool.
    - `__call__()`: Call the _run method with the arguments and return the output.
    - `confirm_before_running()`: Get human confirmation before running the tool. Can be called anywhere in the _run method.

    Example:
    --------
    ```
    class FileReadTool(Tool):
        def __init__(self):
            super().__init__(
                name="File Read",
                desc="Read a file",
                args={"file_path": "The path to the file to be read",
                      "encoding": "(Optional) The encoding of the file"})

        async def _run(self, file_path: str, encoding: str = "utf-8"):
            with open(file_path, "r", encoding=encoding) as f:
                return f.read(), 0

    file_read_tool = FileReadTool()
    await file_read_tool("temp/file.txt")
    """

    def __init__(self, name: str, desc: str, args: Optional[dict] = None):
        self.name = name
        self.desc = desc
        self.args = args
        self._validate_args()

    def _validate_args(self) -> None:
        args = self.args.keys() + ['self']
        argspec = inspect.getfullargspec(self._run)
        arg_names = argspec.args
        if set(arg_names) != set(args):
            raise DefinitionError(f"{self._run.__qualname__} expects arguments: {args},"
                                  f" got: {set(arg_names)}")

    def human_confirmation(self, details: dict) -> None:
        """Asks for human confirmation.

        Arguments:
        ----------
        - `args`: The arguments of the tool.
        - `kwargs`: The keyword arguments of the tool.

        Raises:
        -------
        - `DeniedByUserException`: If the user denies running the tool.
        """
        run_function = input(f"\nTool: {self.__class__.__name__} Details: {details} (y/n): ")
        if run_function.lower() != 'y':
            raise DeniedByUserException(f'Tool: {self.__class__.__name__} Details: {details}')

    async def __call__(self, *args, **kwargs) -> Tuple[Any, int]:
        publish_event('tool_start', data={'name': self.__class__.__name__,
                                          'args': args, 'kwargs': kwargs})

        try:
            output = await self._run(*args, **kwargs)
        except KeyboardInterrupt:
            output = 'Interrupted by User', 1

        if not len(output) == 2:
            raise DefinitionError(f"_run output must be a tuple like (output, exit_code),"
                                  f" got: {output}")
        if output[1] not in [0, 1]:
            raise DefinitionError(f"_run exit code must be 0 or 1, got: {output[1]}")

        publish_event('tool_end', data={'name': self.__class__.__name__, 'output': output,
                                        'args': args, 'kwargs': kwargs})

        return output

    @abstractmethod
    async def _run(self, *args, **kwargs) -> Tuple[Any, int]:
        """This function runs the tool with the arguments and returns the output.

        Use the __call__ method of the tool object to call this method. Do not call this method directly.

        Arguments:
        ----------
        - `args`: The arguments of the tool.
        - `kwargs`: The keyword arguments of the tool.

        Returns:
        --------
        - `output`: The output of the tool.
        - `exit_code` - 0 if the tool ran successfully, 1 if the tool failed.

        Raises:
        -------
        """
        raise NotImplementedError
