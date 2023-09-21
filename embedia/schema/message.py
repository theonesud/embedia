from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """The available roles for a message."""

    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    """The message exchanged between the user and the assistant.

    Attributes
    ----------
    - `role` (`MessageRole`): The role of the message (user / assistant / system)
    - `content` (str): The content of the message.
    - `id` (str, optional): The id of the message. Defaults to a random uuid.
    - `created_at` (str, optional): The timestamp of the message. Defaults to the current time with system's timezone.
    """

    role: MessageRole
    content: str
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(
        default_factory=lambda: str(datetime.now(timezone.utc).astimezone())
    )
