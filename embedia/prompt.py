from pydantic import BaseModel
from typing import Optional


class Prompt(BaseModel):
    template: str
    context: Optional[dict]

    def to_str(self) -> str:
        if self.context is None:
            return self.template
        else:
            return self.template.format(**self.context)
