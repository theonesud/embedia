from pydantic import BaseModel

from embedia.schema.tool import ToolReturn


class Action(BaseModel):
    """The action to be performed by the agent.

    Attributes
    ----------
    - `tool_name` (str): The name of the tool to be used.
    - `args` (dict): The arguments to the tool.
    """
    tool_name: str
    args: dict


class Step(BaseModel):
    """A step in the agent's loop.

    Attributes
    ----------
    - `question` (str): The question that was asked.
    - `action` (`Action`): The action that was performed by the agent.
    - `result` (`ToolReturn`): The result of the action.
    """
    question: str
    action: Action
    result: ToolReturn

    def serialize(self):
        return {'question': self.question,
                'action': dict(self.action),
                'result': dict(self.result)}
