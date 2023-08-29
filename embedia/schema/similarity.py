from enum import Enum


class StringSimilarityMetric(str, Enum):
    DamerauLevenshtein = 'damerau_levenshtein'
    Hamming = 'hamming'
    Indel = 'indel'
    Jaro = 'jaro'
    JaroWinkler = 'jaro_winkler'
    Levenshtein = 'levenshtein'
    Osa = 'osa'
    Prefix = 'prefix'
    Postfix = 'postfix'


class EmbeddingSimilarityMetric(str, Enum):
    Cosine = 'cosine'
    Euclidean = 'euclidean'
    Dot = 'dot'
    Manhattan = 'manhattan'
    Chebyshev = 'chebyshev'
    Hamming = 'hamming'
