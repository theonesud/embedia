from pydantic import BaseModel
import uuid
from enum import Enum
from uuid import uuid4
from datetime import datetime, timezone


class RoleEnum(str, Enum):
    user = 'user'
    assistant = 'assistant'
    system = 'system'


class Message(BaseModel):
    role: RoleEnum
    content: str
    id: uuid.UUID = uuid4()
    created_at: datetime = datetime.now(timezone.utc).astimezone()

    def to_json(self) -> dict:
        return {
            'role': self.role,
            'content': self.content
        }
