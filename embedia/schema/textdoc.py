import copy
import re
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class TextDoc(BaseModel):
    """The text document class with helper functions for text processing.
    Can be used with the `VectorDB` and `EmbeddingModel` classes.

    Attributes
    ----------
    - `contents` (str): The contents of the text document.
    - `meta` (dict, optional): Any metadata related to the text document. Defaults to None.
    - `id` (str, optional): The id of the text document. Defaults to a random uuid.
    - `created_at` (str, optional): The timestamp of the text document. Defaults to the current time with system's timezone.

    Methods
    -------
    - `from_file` (classmethod): Create a `TextDoc` instance from a file.
    - `split_on_separator`: Split the contents on a separator and return a list of `TextDoc` instances.
    - `extract_regex`: Extract `TextDoc` instances from the content using a regex pattern.
    """

    contents: str
    meta: Optional[dict] = None
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(
        default_factory=lambda: str(datetime.now(timezone.utc).astimezone())
    )

    @classmethod
    def from_file(
        cls, path: str, meta: Optional[dict] = None, encoding: str = "utf-8"
    ) -> "TextDoc":
        """Create a `TextDoc` instance from a file.

        Parameters
        ----------
        - `path` (str): The path to the file.
        - `meta` (dict, optional): Any metadata related to the text document. Defaults to None.
        - `encoding` (str, optional): The encoding of the file. Defaults to 'utf-8'.
        """
        with open(path, encoding=encoding) as f:
            instance = cls(meta=meta, contents=f.read())
        return instance

    def split_on_separator(
        self, separator: str = "\n", strip_after_split: bool = False
    ) -> List["TextDoc"]:
        """Split the contents on a separator and return a list of `TextDoc` instances.
        The metadata of the original instance is copied to the split instances.
        A `segment_number` and `parent_id` are added to the metadata of the split instances.

        Parameters
        ----------
        - `separator` (str, optional): The separator to split on. Defaults to '\n'.
        - `strip_after_split` (bool, optional): Whether to strip spaces from the contents after splitting. Defaults to False.

        Returns
        -------
        - `result` (List[TextDoc]): The list of `TextDoc` instances.
        """
        result = []
        for idx, content in enumerate(self.contents.split(separator)):
            if content.strip() == "":
                continue
            elif strip_after_split:
                content = content.strip()
            new_meta = copy.deepcopy(self.meta)
            new_meta["segment_number"] = idx + 1
            new_meta["parent_id"] = self.id
            result.append(TextDoc(contents=content, meta=new_meta))
        return result

    def extract_regex(self, pattern: str) -> List["TextDoc"]:
        """Extract `TextDoc` instances from the content using a regex pattern.
        The metadata of the original instance is copied to the extracted instances.
        A `parent_id` is added to the metadata of the extracted instances.

        Parameters
        ----------
        - `pattern` (str): The regex pattern to use.

        Returns
        -------
        - `result` (List[TextDoc]): The list of `TextDoc` instances.
        """
        new_meta = copy.deepcopy(self.meta)
        new_meta["parent_id"] = self.id
        return [
            TextDoc(contents=content, meta=new_meta)
            for content in re.findall(pattern, self.contents, re.DOTALL)
        ]
