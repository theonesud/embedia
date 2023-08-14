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
    """Message class to store each chat message.

    Arguments:
    ----------
    - `role`: The role of the sender. It can be one of the following:
        - `user`: The message is from the user.
        - `assistant`: The message is from the assistant.
        - `system`: The message is from the system.
    - `content`: The content of the message.
    - `id`: The unique id of the message. It is automatically generated.
    - `created_at`: The timestamp of the message. It is automatically generated.

    Methods:
    --------
    - `to_json`: Convert the message to a JSON object.

    Example:
    --------
    ```
    message = Message(role='user', content='How is the weather today?')
    """
    role: RoleEnum
    content: str
    id: uuid.UUID = uuid4()
    created_at: datetime = datetime.now(timezone.utc).astimezone()

    def to_json(self) -> dict:
        """Convert the message to a JSON object.

        Example:
        --------
        ```
        message = Message(role='user', content='How is the weather today?')
        print(message.to_json())

        >>> {'role': 'user', 'content': 'How is the weather today?'}
        """
        return {
            'role': self.role,
            'content': self.content
        }
