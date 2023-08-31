from typing import Any, Tuple

from pydantic import BaseModel


class Action(BaseModel):
    tool_name: str
    args: dict

    def __str__(self):
        return f"{self.tool_name}: {self.args}"


class ActionStep(BaseModel):
    question: str
    action: Action
    result: Tuple[Any, int]

    def __str__(self):
        if self.result[1] == 0:
            return f"Question: {self.question}\n" \
                   f"Action: {str(self.action)}\n" \
                   f"Result: {self.result[0]}"
        else:
            return f"Question: {self.question}\n" \
                   f"Action: {str(self.action)}\n" \
                   f"Error: {self.result[0]}"
