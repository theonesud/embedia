from typing import Any, List, Optional

from pydantic import BaseModel


class VectorDBInsert(BaseModel):
    """The data to be inserted into the vector database.
    The embedding is not required if the database can embed the data itself.

    Attributes
    ----------
    - `id` (str): The id of the data.
    - `text` (str): The text of the data.
    - `embedding` (List[Any], optional): The embedding of the data. Defaults to None.
    - `meta` (dict, optional): Any metadata related to the text. Defaults to None.
    """

    id: str
    text: str
    embedding: Optional[List[Any]] = None
    meta: Optional[dict] = None


class VectorDBGetSimilar(BaseModel):
    """The data to be used to get similar data from the vector database.
    Provide either the text or the embedding.

    Attributes
    ----------
    - `text` (str, optional): The text you want to vector search for. Defaults to None.
    - `embedding` (List[Any], optional): The embedding you want to vector search for. Defaults to None.
    - `n_results` (int, optional): The number of results to return. Defaults to 5.
    """

    text: Optional[str] = None
    embedding: Optional[List[Any]] = None
    n_results: int = 5
