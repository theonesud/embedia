from pydantic import BaseModel
from typing import List, Any, Optional


class VectorDBInsert(BaseModel):
    id: str
    text: str
    embedding: Optional[List[Any]] = None
    meta: Optional[dict] = None


class VectorDBGetSimilar(BaseModel):
    text: Optional[str] = None
    embedding: Optional[List[Any]] = None
    n_results: int = 5
