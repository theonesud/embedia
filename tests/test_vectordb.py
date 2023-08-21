import os

import chromadb
import openai
import pytest
import tiktoken
from dotenv import load_dotenv
from tenacity import (retry, retry_if_not_exception_type, stop_after_attempt,
                      wait_random_exponential)

from embedia import EmbeddingModel, Tokenizer, VectorDB
from embedia.utils.vectordb import distance_to_similarity

load_dotenv()
os.makedirs('temp/chromadb', exist_ok=True)

text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eu arcu risus. Proin sed fringilla tellus. Donec scelerisque elit sed sapien bibendum rutrum. Morbi blandit justo in urna semper volutpat. Nunc consectetur ex vitae consequat blandit. Duis sit amet metus quis mi molestie bibendum rutrum et ante. Nam aliquam metus magna, eget porta lacus dictum sit amet. Morbi dictum tellus a semper tristique. Duis ipsum ex, pharetra non rhoncus in, gravida quis magna. Nam pretium enim non lectus efficitur, sit amet sagittis elit finibus. Vivamus varius ligula turpis, sit amet vehicula mi eleifend eget. Cras dignissim mauris eu feugiat euismod. Integer dapibus dolor eu nulla euismod finibus. """

complete_text = text * 50


@pytest.mark.asyncio
async def test_create_embedding():
    embedding_model = OpenAIEmbedding()
    embedding = await embedding_model(complete_text)
    assert len(embedding) == 1536

    # collection_metadata = {"hnsw:space": "ip"}
    # collection_metadata = {"hnsw:space": "cosine"}
    collection_metadata = {"hnsw:space": "l2"}
    db = ChromaDB('temp/chromadb', 'Embedia', collection_metadata)

    await db.save_embeddings(embedding, {'lorem': 'ipsum'}, complete_text, '1')

    docs = db.collection.get(ids=["1"], include=["documents", "embeddings", "metadatas"])
    assert docs['ids'] == ['1']
    assert docs['documents'] == [complete_text]
    assert len(docs['embeddings'][0]) == 1536

    query = await embedding_model('Lorem Ipsum')
    results = await db.similarity_search(query)
    assert results['ids'] == [['1']]
    assert results['documents'] == [[complete_text]]
    assert results['metadatas'] == [[{'lorem': 'ipsum'}]]
    similarity_score = distance_to_similarity(results['distances'][0][0], 'l2')
    assert similarity_score > 0.8
