from pydantic import BaseModel
from embedia.schema.tool import ToolReturn


class Action(BaseModel):
    tool_name: str
    args: dict


class Step(BaseModel):
    question: str
    action: Action
    result: ToolReturn

    def serialize(self):
        return {'question': self.question,
                'action': dict(self.action),
                'result': dict(self.result)}
