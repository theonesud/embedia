from pydantic import BaseModel
from typing import List, Literal, Optional, Any


class ArgDocumentation(BaseModel):
    name: str
    desc: str


class ToolDocumentation(BaseModel):
    name: str
    desc: str
    args: Optional[List[ArgDocumentation]] = None


class ToolReturn(BaseModel):
    output: Any
    exit_code: Literal[0, 1] = 0
