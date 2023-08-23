from abc import ABC, abstractmethod
from typing import List, Union

import numpy as np
import json

from embedia.core.tokenizer import Tokenizer
from embedia.schema.textdoc import TextDoc
from embedia.utils.pubsub import publish_event
from embedia.utils.exceptions import DefinitionError


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

    async def __call__(self, input: Union[TextDoc, str]) -> List[float]:
        if isinstance(input, TextDoc):
            input = input.contents
            if input.meta:
                meta_str = json.dumps(input.meta)
                input = 'metadata:' + meta_str + '\n' + 'content:' + input
        elif isinstance(input, str):
            pass
        else:
            raise DefinitionError(f"Input should be of type TextDoc or str. Got: {type(input)}")

        tokens = await self.tokenizer(input)
        publish_event('embedding_start', data={'input': input, 'num_tokens': len(tokens)})

        if (len(tokens) > self.max_input_tokens):
            tokens_split = []
            for j in range(0, len(tokens), self.max_input_tokens):
                tokens_split.append(tokens[j:j + self.max_input_tokens])
            embeddings = []
            lengths = []
            for chunk in tokens_split:
                # TODO: check if _embed can take a List[int] as input
                # TODO: check the difference between sending str vs List[int] to embedding api
                resp = await self._embed(chunk)

                if not isinstance(resp, list):
                    raise DefinitionError(f"_embed output must be a list, got: {type(resp)}")
                if resp and not isinstance(resp[0], float):
                    raise DefinitionError(f"_embed output must be a list of floats, got: {type(resp[0])}")

                embeddings.append(resp)
                lengths.append(len(chunk))
            embedding = np.average(embeddings, axis=0, weights=lengths)
            embedding = embedding / np.linalg.norm(embedding)
            embedding = embedding.tolist()
        else:

            embedding = await self._embed(tokens)

            if not isinstance(resp, list):
                raise DefinitionError(f"_embed output must be a list, got: {type(resp)}")
            if resp and not isinstance(resp[0], float):
                raise DefinitionError(f"_embed output must be a list of floats, got: {type(resp[0])}")

        publish_event('embedding_end', data={'embedding': embedding})

    @abstractmethod
    async def _embed(self, input: Union[str, List[int]]) -> List[float]:
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
        raise NotImplementedError
