from pydantic import BaseModel
from typing import Optional


class ScratchpadEntry(BaseModel):
    question: Optional[str]
    thought: Optional[str]
    tool: Optional[str]
    args: Optional[str]
    answer: str = 'Sorry, I could not find an answer to your question'
