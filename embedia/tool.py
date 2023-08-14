from abc import ABC, abstractmethod
from typing import Optional, Type
from embedia import ChatLLM
import inspect
from embedia.utils.pubsub import publish_event
from embedia.utils.typechecking import enforce_class_type


class DeniedByUserException(Exception):
    pass


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

    def __init__(self, name: str, desc: str,
                 args: Optional[dict] = None,
                 chatllm: Optional[Type[ChatLLM]] = None):
        enforce_class_type(chatllm, ChatLLM)
        self.chatllm = chatllm
        self.name = name
        self.desc = desc
        self.args = args

    def confirm_before_running(self, *args, **kwargs):
        """Asks for human confirmation.

        Arguments:
        ----------
        - `args`: The arguments of the tool.
        - `kwargs`: The keyword arguments of the tool.

        Raises:
        -------
        - `DeniedByUserException`: If the user denies running the tool.
        """
        run_function = input(
            f"Run {self.__class__.__name__} with args: {args} and kwargs: {kwargs} (y/n): ")
        if run_function.lower() != 'y':
            raise DeniedByUserException(
                f'User denied running function: {self.__class__.__name__} with args: {args} '
                f'and kwargs: {kwargs}')

    async def __call__(self, *args, **kwargs):
        publish_event('tool_start', data={
                      'name': self.__class__.__name__, 'args': args, 'kwargs': kwargs})
        argspec = inspect.getfullargspec(self._run)
        arg_names = argspec.args
        for arg_name in arg_names:
            if arg_name == 'self':
                continue
            if arg_name not in self.args.keys():
                raise ValueError(f"Argument: {arg_name} not found in args docsting: {self.args}")

        output = await self._run(*args, **kwargs)
        assert len(output) == 2, ("Output must be a tuple of length 2 like (output, exit_code),"
                                  f" got: {output}")
        assert output[1] in [0, 1], f"Exit code must be 0 or 1, got: {output[1]}"
        publish_event('tool_end', data={'name': self.__class__.__name__, 'output': output})
        return output

    @abstractmethod
    async def _run(self):
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
        - `ValueError`: If the arguments are not added to the docstring.
        - `AssertionError`: If the output is not a tuple of length 2 like (output, exit_code).
        - `AssertionError`: If the exit_code is not 0 or 1.
        """
        pass
