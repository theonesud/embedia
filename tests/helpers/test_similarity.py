import pytest

from embedia import (EmbeddingSimilarityMetric, StringSimilarityMetric,
                     embedding_similarity, string_similarity)
from embedia.utils.exceptions import DefinitionError
from tests.core.definitions import OpenAIEmbedding


@pytest.mark.asyncio
async def test_str_similarity():
    a = 'Artificial Intelligence will take over the world'
    b = 'Artificial Intelligence is taking over the world'
    sim = await string_similarity(a, b, StringSimilarityMetric.JaroWinkler)
    print(sim)
    assert sim > 0.92
    sim = await string_similarity(a, b, StringSimilarityMetric.DamerauLevenshtein)
    print(sim)
    assert sim == 0.875
    sim = await string_similarity(a, b, StringSimilarityMetric.Hamming)
    print(sim)
    assert sim == 0.8125
    sim = await string_similarity(a, b, StringSimilarityMetric.Indel)
    print(sim)
    assert sim > 0.91
    sim = await string_similarity(a, b, StringSimilarityMetric.Jaro)
    print(sim)
    assert sim > 0.87
    sim = await string_similarity(a, b, StringSimilarityMetric.Levenshtein)
    print(sim)
    assert sim == 0.875
    sim = await string_similarity(a, b, StringSimilarityMetric.Osa)
    print(sim)
    assert sim == 0.875
    sim = await string_similarity(a, b, StringSimilarityMetric.Prefix)
    print(sim)
    assert sim == 0.5
    sim = await string_similarity(a, b, StringSimilarityMetric.Postfix)
    print(sim)
    assert sim == 0.3125


@pytest.mark.asyncio
async def test_str_similarity_error():
    a = 'Artificial Intelligence will take over the world'
    b = 'Artificial Intelligence is taking over the world'
    with pytest.raises(DefinitionError) as e:
        await string_similarity(a, b, 'unknown')
    print(e)
    with pytest.raises(DefinitionError) as e:
        await string_similarity(5, b)
    print(e)
    with pytest.raises(DefinitionError) as e:
        await string_similarity(a, 6)
    print(e)


@pytest.mark.asyncio
async def test_emb_similarity():
    a = 'Artificial Intelligence will take over the world'
    b = 'Artificial Intelligence is taking over the world'
    emb = OpenAIEmbedding()
    emb_a = await emb(a)
    emb_b = await emb(b)
    sim = await embedding_similarity(emb_a, emb_b, EmbeddingSimilarityMetric.Cosine)
    print(sim)
    assert sim > 0.98
    sim = await embedding_similarity(emb_a, emb_b, EmbeddingSimilarityMetric.Euclidean)
    print(sim)
    assert sim > 0.83
    sim = await embedding_similarity(emb_a, emb_b, EmbeddingSimilarityMetric.Dot)
    print(sim)
    assert sim > 0.72
    sim = await embedding_similarity(emb_a, emb_b, EmbeddingSimilarityMetric.Manhattan)
    print(sim)
    assert sim > 0.14
    sim = await embedding_similarity(emb_a, emb_b, EmbeddingSimilarityMetric.Chebyshev)
    print(sim)
    assert sim > 0.98
    sim = await embedding_similarity(emb_a, emb_b, EmbeddingSimilarityMetric.Hamming)
    print(sim)
    assert sim == 0


@pytest.mark.asyncio
async def test_emb_similarity_error():
    with pytest.raises(DefinitionError) as e:
        emb_a = [1, 2, 3]
        emb_b = [1, 2, 3]
        await embedding_similarity(emb_a, emb_b, 'unknown')
    print(e)
    with pytest.raises(DefinitionError) as e:
        emb_a = [1, 2, 3]
        emb_b = [1, 2, 3, 4]
        await embedding_similarity(emb_a, emb_b, 'unknown')
    print(e)
    emb_a = [0, 0, 0, 0]
    emb_b = [1, 2, 3, 4]
    sim = await embedding_similarity(emb_a, emb_b, 'unknown')
    assert sim == 0
    with pytest.raises(DefinitionError) as e:
        emb_a = '[1, 2, 3]'
        emb_b = [1, 2, 3]
        await embedding_similarity(emb_a, emb_b)
    print(e)
    with pytest.raises(DefinitionError) as e:
        emb_a = [1, 2, 3]
        emb_b = '[1, 2, 3]'
        await embedding_similarity(emb_a, emb_b)
    print(e)
