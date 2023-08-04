from pydantic import BaseModel
import uuid
from uuid import uuid4
from datetime import datetime, timezone


class Message(BaseModel):
    role: str
    content: str
    id: uuid.UUID = uuid4()
    created_at: datetime = datetime.now(timezone.utc).astimezone()

    def to_json(self) -> dict:
        return {
            'role': self.role,
            'content': self.content
        }
