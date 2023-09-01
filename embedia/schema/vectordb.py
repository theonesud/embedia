from pydantic import BaseModel
from typing import List, Any, Optional


class VectorDBInsert(BaseModel):
    id: str
    text: str
    embedding: List[Any]
    meta: Optional[dict] = None


class VectorDBGetSimilar(BaseModel):
    embedding: List[Any]
    n_results: int = 5
