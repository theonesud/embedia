from abc import ABC, abstractmethod
from embedia import Tokenizer
from typing import List
import numpy as np
import logging


class EmbeddingModel(ABC):
    def __init__(self, max_input_tokens: int, tokenizer: Tokenizer):
        self.max_input_tokens = max_input_tokens
        self.tokenizer = tokenizer

    @abstractmethod
    async def _embed(self):
        pass

    async def __call__(self, text, split_and_average=True) -> List[float]:
        tokens = await self.tokenizer(text)
        if (len(tokens) > self.max_input_tokens) and split_and_average:
            logging.warning("Input text is too long. It will be split into chunks.")
            tokens_split = []
            for j in range(0, len(tokens), self.max_input_tokens):
                tokens_split.append(tokens[j:j + self.max_input_tokens])
            embeddings = []
            lengths = []
            for chunk in tokens_split:
                embeddings.append(await self._embed(chunk))
                lengths.append(len(chunk))
            embeddings = np.average(embeddings, axis=0, weights=lengths)
            embeddings = embeddings / np.linalg.norm(embeddings)
            embeddings = embeddings.tolist()
            return embeddings
        else:
            return await self._embed(text)


class VectorDB(ABC):

    async def save_embeddings(self, *args, **kwargs):
        return await self._save_embeddings(*args, **kwargs)

    async def similarity_search(self, *args, **kwargs):
        return await self._similarity_search(*args, **kwargs)

    @abstractmethod
    async def _save_embeddings(self):
        pass

    @abstractmethod
    async def _similarity_search(self):
        pass
