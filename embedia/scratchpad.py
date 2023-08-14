from pydantic import BaseModel


class ScratchpadEntry(BaseModel):
    question: str
    tool: str
    args: dict
    observation: tuple
