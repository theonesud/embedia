import copy
import re
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel


class TextDoc(BaseModel):
    contents: str
    meta: Optional[dict] = None
    id: uuid.UUID = uuid4()
    created_at: datetime = datetime.now(timezone.utc).astimezone()

    @classmethod
    def from_file(cls, path: str, meta: Optional[dict] = None, encoding: str = 'utf-8') -> 'TextDoc':
        with open(path, 'r', encoding=encoding) as f:
            instance = cls(meta=meta, contents=f.read())
        return instance

    # add splitter for coding languages

    def split_on_separator(self, separator: str = '\n', strip_spaces: bool = True) -> List['TextDoc']:
        result = []
        for idx, content in enumerate(self.contents.split(separator)):
            if content.strip() == '':
                continue
            elif strip_spaces:
                content = content.strip()
            new_meta = copy.deepcopy(self.meta)
            new_meta['segment_number'] = idx + 1
            new_meta['parent_id'] = self.id
            result.append(TextDoc(contents=self.contents, meta=new_meta))
        return result

    def extract_regex(self, pattern: str) -> List['TextDoc']:
        new_meta = copy.deepcopy(self.meta)
        new_meta['parent_id'] = self.id
        return [TextDoc(contents=content, meta=new_meta) for
                content in re.findall(pattern, self.contents, re.DOTALL)]
