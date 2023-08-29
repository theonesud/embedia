import tiktoken
from dotenv import load_dotenv
import os
import openai
import time
import chromadb
from typing import List
from embedia import Tokenizer, LLM, ChatLLM, Tool, EmbeddingModel, VectorDB, TextDoc
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

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return completion.choices[0].message.content


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
        await self.human_confirmation(details={'text': text})
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


class OpenAITokenizerBroken1(Tokenizer):
    def __init__(self):
        super().__init__()

    async def _tokenize(self) -> List[int]:
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode('text')


class OpenAITokenizerBroken2(Tokenizer):
    def __init__(self):
        super().__init__()

    async def _tokenize(self, text: str) -> List[int]:
        return 'asd'


class OpenAILLMBroken1(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer,
                         max_input_tokens=4000)

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAILLMBroken2(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens='4000')

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAILLMBroken3(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=0)

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAILLMBroken4(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4000)

    async def _complete(self) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt='prompt',
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAILLMBroken5(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4000)

    async def _complete(self, prompt: str) -> str:
        return [1, 2, 3]


class OpenAIChatLLMBroken1(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer,
                         max_input_tokens=4096)

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return completion.choices[0].message.content


class OpenAIChatLLMBroken2(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens='4096')

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return completion.choices[0].message.content


class OpenAIChatLLMBroken3(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=0)

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return completion.choices[0].message.content


class OpenAIChatLLMBroken4(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4096)

    async def _reply(self) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return completion.choices[0].message.content


class OpenAIChatLLMBroken5(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4096)

    async def _reply(self, prompt: str) -> str:
        return 44


class PrintToolBroken1(Tool):
    def __init__(self):
        super().__init__(name=3,
                         desc="Prints whatever you give it",
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class PrintToolBroken2(Tool):
    def __init__(self):
        super().__init__(name="",
                         desc="Prints whatever you give it",
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class PrintToolBroken3(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc=4,
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class PrintToolBroken4(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="",
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class PrintToolBroken5(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args="The text to be printed. Type: String")

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class PrintToolBroken6(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args={4: "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class PrintToolBroken7(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args={"text": 5})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class PrintToolBroken8(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args={"texts": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0


class PrintToolBroken9(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return [None, 0]


class PrintToolBroken10(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 0, 8


class PrintToolBroken11(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, '0'


class PrintToolBroken12(Tool):
    def __init__(self):
        super().__init__(name="Print Tool",
                         desc="Prints whatever you give it",
                         args={"text": "The text to be printed. Type: String"})

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return None, 4


class OpenAIEmbeddingBroken1(EmbeddingModel):
    def __init__(self):
        super().__init__()

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
           retry=retry_if_not_exception_type(openai.InvalidRequestError))
    async def _embed(self):
        result = await openai.Embedding.acreate(input=input, model='text-embedding-ada-002')
        return result["data"][0]["embedding"]


class OpenAIEmbeddingBroken2(EmbeddingModel):
    def __init__(self):
        super().__init__()

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
           retry=retry_if_not_exception_type(openai.InvalidRequestError))
    async def _embed(self, input: str):
        return 'asd'


class ChromaDBBroken1(VectorDB):
    def __init__(self):
        super().__init__()
        self.client = chromadb.PersistentClient(path='temp/chromadb')
        self.collection = self.client.get_or_create_collection(
            name='Embedia', metadata={"hnsw:space": "l2"})

    async def _insert(self, text, metadata, embedding):
        self.collection.upsert(metadatas=[metadata], embeddings=[embedding], documents=[text], ids=['id'])

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


class ChromaDBBroken2(VectorDB):
    def __init__(self):
        super().__init__()
        self.client = chromadb.PersistentClient(path='temp/chromadb')
        self.collection = self.client.get_or_create_collection(
            name='Embedia', metadata={"hnsw:space": "l2"})

    async def _insert(self, id, text, metadata, embedding):
        self.collection.upsert(metadatas=[metadata], embeddings=[embedding], documents=[text], ids=[id])

    async def _get_similar(self, n_results):
        resp = self.collection.query(query_embeddings=['embedding'], n_results=n_results,
                                     include=["metadatas", "documents", "distances"])
        result = []
        for i in range(len(resp["ids"][0])):
            doc = TextDoc(id=resp["ids"][0][i], contents=resp["documents"][0][i],
                          meta=resp["metadatas"][0][i])
            similarity = 1 / (1 + resp["distances"][0][i])
            result.append((similarity, doc))
        return result


class ChromaDBBroken3(VectorDB):
    def __init__(self):
        super().__init__()
        self.client = chromadb.PersistentClient(path='temp/chromadb')
        self.collection = self.client.get_or_create_collection(
            name='Embedia', metadata={"hnsw:space": "l2"})

    async def _insert(self, id, text, metadata, embedding):
        self.collection.upsert(metadatas=[metadata], embeddings=[embedding], documents=[text], ids=[id])

    async def _get_similar(self, embedding, n_results):
        return 'asd'

# TODO: write all broken classes
# TODO: check coverage
