from rapidfuzz.distance import DamerauLevenshtein, Hamming, Indel, Jaro, JaroWinkler, Levenshtein, OSA, Prefix, Postfix
from typing import List
import numpy as np
from embedia.utils.typechecking import check_type
from embedia.schema.similarity import StringSimilarityMetric, EmbeddingSimilarityMetric


async def string_similarity(s1: str, s2: str, method: StringSimilarityMetric = StringSimilarityMetric.JaroWinkler) -> float:
    check_type(s1, str, string_similarity)
    check_type(s2, str, string_similarity)
    if method == StringSimilarityMetric.DamerauLevenshtein:
        return DamerauLevenshtein.normalized_similarity(s1, s2)
    elif method == StringSimilarityMetric.Hamming:
        return Hamming.normalized_similarity(s1, s2)
    elif method == StringSimilarityMetric.Indel:
        return Indel.normalized_similarity(s1, s2)
    elif method == StringSimilarityMetric.Jaro:
        return Jaro.normalized_similarity(s1, s2)
    elif method == StringSimilarityMetric.JaroWinkler:
        return JaroWinkler.normalized_similarity(s1, s2)
    elif method == StringSimilarityMetric.Levenshtein:
        return Levenshtein.normalized_similarity(s1, s2)
    elif method == StringSimilarityMetric.Osa:
        return OSA.normalized_similarity(s1, s2)
    elif method == StringSimilarityMetric.Prefix:
        return Prefix.normalized_similarity(s1, s2)
    elif method == StringSimilarityMetric.Postfix:
        return Postfix.normalized_similarity(s1, s2)
    else:
        raise ValueError(f"Unknown method: {method}")


async def embedding_similarity(e1: List[float], e2: List[float], method: EmbeddingSimilarityMetric = EmbeddingSimilarityMetric.Cosine) -> float:
    check_type(e1, list, embedding_similarity)
    check_type(e2, list, embedding_similarity)
    if len(e1) != len(e2):
        raise ValueError("Embeddings must have the same dimensionality")
    e1 = np.array(e1)
    e2 = np.array(e2)
    if np.linalg.norm(e1) == 0 or np.linalg.norm(e2) == 0:
        return 0

    if method == EmbeddingSimilarityMetric.Cosine:
        return np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
    elif method == EmbeddingSimilarityMetric.Euclidean:
        return 1 / (1 + np.linalg.norm(e1 - e2))
    elif method == EmbeddingSimilarityMetric.Dot:
        return 1 / (1 + np.exp(-np.dot(e1, e2)))
    elif method == EmbeddingSimilarityMetric.Manhattan:
        return 1 / (1 + np.sum(np.abs(e1 - e2)))
    elif method == EmbeddingSimilarityMetric.Chebyshev:
        return 1 / (1 + np.max(np.abs(e1 - e2)))
    elif method == EmbeddingSimilarityMetric.Hamming:
        return 1 - np.sum(e1 != e2) / len(e1)
    else:
        raise ValueError(f"Unknown method: {method}")
