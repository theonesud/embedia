import pytest
import openai
import tiktoken
from embedia.vectordb import VectorDB, EmbeddingModel
from embedia.tokenizer import Tokenizer
import os
from embedia.utils.vectordb import distance_to_similarity
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type
import chromadb
import numpy as np
from dotenv import load_dotenv
load_dotenv()
os.makedirs('temp/chromadb', exist_ok=True)

text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eu arcu risus. Proin sed fringilla tellus. Donec scelerisque elit sed sapien bibendum rutrum. Morbi blandit justo in urna semper volutpat. Nunc consectetur ex vitae consequat blandit. Duis sit amet metus quis mi molestie bibendum rutrum et ante. Nam aliquam metus magna, eget porta lacus dictum sit amet. Morbi dictum tellus a semper tristique. Duis ipsum ex, pharetra non rhoncus in, gravida quis magna. Nam pretium enim non lectus efficitur, sit amet sagittis elit finibus. Vivamus varius ligula turpis, sit amet vehicula mi eleifend eget. Cras dignissim mauris eu feugiat euismod. Integer dapibus dolor eu nulla euismod finibus. """

complete_text = text*50


class GPTTokenizer(Tokenizer):
    async def _tokenize(self, text):
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return enc.encode(text, allowed_special=set(),
                          disallowed_special='all')


class OpenAIEmbedding(EmbeddingModel):

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
           retry=retry_if_not_exception_type(openai.InvalidRequestError))
    async def _embed(self, text):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        result = await openai.Embedding.acreate(input=text, model='text-embedding-ada-002')
        return result["data"][0]["embedding"]


class ChromaDB(VectorDB):
    def __init__(self, db_path, collection_name, collection_metadata):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata=collection_metadata)

    async def _save_embeddings(self, embeddings, metadatas, texts, ids):
        # can add a single / list of embeddings, metadatas, texts, ids
        self.collection.upsert(metadatas=metadatas, embeddings=embeddings, documents=texts, ids=ids)

    async def _similarity_search(self, embeddings, k=5):
        return self.collection.query(query_embeddings=embeddings, n_results=k)


@pytest.mark.asyncio
async def test_create_embedding():
    embedding_model = OpenAIEmbedding(max_input_tokens=8191,
                                      tokenizer=GPTTokenizer())
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
    print(similarity_score)
