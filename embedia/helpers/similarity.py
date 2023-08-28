from rapidfuzz.distance import DamerauLevenshtein, Hamming, Indel, Jaro, JaroWinkler, Levenshtein, OSA, Prefix, Postfix
from typing import List
import numpy as np
from embedia.utils.exceptions import DefinitionError


def string_similarity(s1: str, s2: str, method="jaro_winkler") -> float:
    if method == "damerau_levenshtein":
        return DamerauLevenshtein.normalized_similarity(s1, s2)
    elif method == "hamming":
        return Hamming.normalized_similarity(s1, s2)
    elif method == "indel":
        return Indel.normalized_similarity(s1, s2)
    elif method == "jaro":
        return Jaro.normalized_similarity(s1, s2)
    elif method == "jaro_winkler":
        return JaroWinkler.normalized_similarity(s1, s2)
    elif method == "levenshtein":
        return Levenshtein.normalized_similarity(s1, s2)
    elif method == "osa":
        return OSA.normalized_similarity(s1, s2)
    elif method == "prefix":
        return Prefix.normalized_similarity(s1, s2)
    elif method == "postfix":
        return Postfix.normalized_similarity(s1, s2)
    else:
        raise DefinitionError(f"Unknown method: {method}")


def embedding_similarity(e1: List[float], e2: List[float], method='cosine') -> float:
    if len(e1) != len(e2):
        raise DefinitionError("Embeddings must have the same dimensionality")
    e1 = np.array(e1)
    e2 = np.array(e2)
    if np.linalg.norm(e1) == 0 or np.linalg.norm(e2) == 0:
        return 0

    if method == 'cosine':
        return np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
    elif method == 'euclidean':
        return 1 / (1 + np.linalg.norm(e1 - e2))
    elif method == 'dot':
        return 1 / (1 + np.exp(-np.dot(e1, e2)))
    elif method == 'manhattan':
        return 1 / (1 + np.sum(np.abs(e1 - e2)))
    elif method == 'chebyshev':
        return 1 / (1 + np.max(np.abs(e1 - e2)))
    elif method == 'hamming':
        return 1 - np.sum(e1 != e2) / len(e1)
    else:
        raise DefinitionError(f"Unknown method: {method}")

# TODO: make them enum
