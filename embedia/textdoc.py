from pydantic import BaseModel
from uuid import uuid4
import uuid
from datetime import datetime, timezone
from typing import Optional
import re


class TextDoc(BaseModel):
    name: str
    description: str
    contents: str
    src: str
    id: uuid.UUID = uuid4()
    parent_id: Optional[uuid.UUID] = None
    parent_segment_number: Optional[int] = None
    created_at: datetime = datetime.now(timezone.utc).astimezone()

    @classmethod
    def from_file(cls, path: str, name: str, description: str, src: str, encoding: str = 'utf-8'):
        with open(path, 'r', encoding=encoding) as f:
            instance = cls(name=name, description=description, contents=f.read(), src=src)
        return instance

    def split_on_separator(self, separator: str = '\n', strip_spaces=True) -> list:
        result = []
        for idx, content in enumerate(self.contents.split(separator)):
            if content.strip() == '':
                continue
            elif strip_spaces:
                content = content.strip()
            result.append(TextDoc(name=self.name, description=self.description,
                          contents=content, src=self.src, parent_id=self.id,
                          parent_segment_number=idx+1))
        return result

    def extract_regex(self, pattern: str) -> list:
        return [TextDoc(name=self.name, description=self.description,
                        contents=content, src=self.src, parent_id=self.id) for
                content in re.findall(pattern, self.contents, re.DOTALL)]
