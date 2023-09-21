from typing import Any, List, Literal, Optional

from pydantic import BaseModel


class ParamDocumentation(BaseModel):
    """The documentation for a function parameter.

    Attributes
    ----------
    - `name` (str): The name of the parameter.
    - `desc` (str): The description of the parameter.
    """

    name: str
    desc: str


class ToolDocumentation(BaseModel):
    """The documentation for a tool.

    Attributes
    ----------
    - `name` (str): The name of the tool.
    - `desc` (str): The description of the tool.
    - `params` (List[`ParamDocumentation`], optional): Documentation of the parameters of the tool.
    """

    name: str
    desc: str
    params: Optional[List[ParamDocumentation]] = None


class ToolReturn(BaseModel):
    """The return type of a tool.

    Attributes
    ----------
    - `output` (Any): The output of the tool.
    - `exit_code` (Literal[0, 1]): The exit code of the tool (0: success, 1: failure)
    """

    output: Any
    exit_code: Literal[0, 1] = 0
