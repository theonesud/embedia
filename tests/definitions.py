import tiktoken
from dotenv import load_dotenv
import os
import openai
import time
import chromadb
from typing import List
from embedia import Tokenizer, LLM, ChatLLM, Message, Tool, EmbeddingModel, VectorDB, TextDoc
from tenacity import (retry, retry_if_not_exception_type, stop_after_attempt,
                      wait_random_exponential)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# TODO: make this setup and teardown
os.makedirs('temp', exist_ok=True)


class OpenAITokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

    async def _tokenize(self, text: str) -> List[int]:
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)


class OpenAILLM(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4000)

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAIChatLLM(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4096)

    async def _reply(self, message: Message) -> Message:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


class SleepTool(Tool):
    def __init__(self):
        super().__init__(name="Sleep Tool",
                         desc="Sleeps for 1 second")

    async def _run(self):
        print("Sleeping for 1 second...")
        time.sleep(1)
        return None, 0


class PrintTool(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class OpenAIEmbedding(EmbeddingModel):
    def __init__(self):
        super().__init__()

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
           retry=retry_if_not_exception_type(openai.InvalidRequestError))
    async def _embed(self, input: str):
        result = await openai.Embedding.acreate(input=input, model='text-embedding-ada-002')
        return result["data"][0]["embedding"]


class ChromaDB(VectorDB):
    def __init__(self):
        super().__init__()
        self.client = chromadb.PersistentClient(path='temp/chromadb')
        self.collection = self.client.get_or_create_collection(
            name='Embedia', metadata={"hnsw:space": "l2"})

    async def _insert(self, id, text, metadata, embedding):
        self.collection.upsert(metadatas=[metadata], embeddings=[embedding], documents=[text], ids=[id])

    async def _get_similar(self, embedding, n_results):
        resp = self.collection.query(query_embeddings=[embedding], n_results=n_results,
                                     include=["metadatas", "documents", "distances"])
        result = []
        for i in range(len(resp["ids"][0])):
            doc = TextDoc(id=resp["ids"][0][i], contents=resp["documents"][0][i],
                          meta=resp["metadatas"][0][i])
            similarity = 1 / (1 + resp["distances"][0][i])
            result.append((similarity, doc))
        return result


# TODO: write all broken classes
# TODO: check coverage
