from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    user = 'user'
    assistant = 'assistant'
    system = 'system'


class Message(BaseModel):

    role: MessageRole
    content: str
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).astimezone()))

    def to_json(self) -> dict:

        return {
            'role': self.role,
            'content': self.content
        }
