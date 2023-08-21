from abc import ABC, abstractmethod
from typing import List

import numpy as np

from embedia.core.tokenizer import Tokenizer
from embedia.schema.textdoc import TextDoc


class EmbeddingModel(ABC):
    """Abstract class for embedding models.

    Arguments:
    ----------
    - `max_input_tokens`: The maximum number of tokens allowed in the input message.
    - `tokenizer`: An object of the `Tokenizer` class used for counting number of tokens.

    Methods:
    --------
    - `_embed()`: Implement this method to return the embedding of the inputs.
    - `__call__()`: This method will call the _embed() internally.
    """

    def __init__(self, max_input_tokens: int, tokenizer: Tokenizer) -> None:
        self.max_input_tokens = max_input_tokens
        self.tokenizer = tokenizer

    @abstractmethod
    async def _embed(self):
        """This function calls the embedding model with the input
        and returns the embedding.

        Use the __call__ method of the EmbeddingModel object to call this method. Do not call this method directly.

        Arguments:
        ----------
        - `input`: The input to be passed to the embedding model.

        Returns:
        --------
        - `embedding`: The embedding of the input.
        """
        pass

    async def __call__(self, textdoc: TextDoc) -> List[float]:
        tokens = await self.tokenizer(textdoc.contents)
        if (len(tokens) > self.max_input_tokens):
            tokens_split = []
            for j in range(0, len(tokens), self.max_input_tokens):
                tokens_split.append(tokens[j:j + self.max_input_tokens])
            embeddings = []
            lengths = []
            for chunk in tokens_split:
                embeddings.append(await self._embed(chunk))
                lengths.append(len(chunk))
            embedding = np.average(embeddings, axis=0, weights=lengths)
            embedding = embedding / np.linalg.norm(embedding)
            embedding = embedding.tolist()
            return embedding
        else:
            return await self._embed(tokens)
