from typing import Any, List, Optional

from pydantic import BaseModel


class VectorDBInsert(BaseModel):
    id: str
    text: str
    embedding: Optional[List[Any]] = None
    meta: Optional[dict] = None


class VectorDBGetSimilar(BaseModel):
    text: Optional[str] = None
    embedding: Optional[List[Any]] = None
    n_results: int = 5
