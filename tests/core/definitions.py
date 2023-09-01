from weaviate.embedded import EmbeddedOptions
import weaviate
import os
import time
from typing import List

import openai
import tiktoken
from dotenv import load_dotenv
from tenacity import (retry, retry_if_not_exception_type, stop_after_attempt,
                      wait_random_exponential)

from embedia import (LLM, ChatLLM, EmbeddingModel, TextDoc, Tokenizer, Tool,
                     VectorDB, ToolDocumentation, ArgDocumentation, ToolReturn,
                     VectorDBInsert, VectorDBGetSimilar)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


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
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


class SleepTool(Tool):
    def __init__(self):
        super().__init__(docs={
            'name': 'Sleep Tool',
            'desc': 'Sleeps for 1 second'
        })

    async def _run(self):
        print("Sleeping for 1 second...")
        time.sleep(1)
        return {'output': 'done'}


class PrintTool(Tool):
    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Sleep Tool",
            desc="Sleeps for 1 second",
            args=[ArgDocumentation(name="text", desc="The text to be printed. Type: String")]))

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return ToolReturn(output='done')


class OpenAIEmbedding(EmbeddingModel):
    def __init__(self):
        super().__init__()

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
           retry=retry_if_not_exception_type(openai.InvalidRequestError))
    async def _embed(self, input: str):
        result = await openai.Embedding.acreate(input=input, model='text-embedding-ada-002')
        return result["data"][0]["embedding"]


class WeaviateDB(VectorDB):
    def __init__(self):
        super().__init__()
        client = weaviate.Client(embedded_options=EmbeddedOptions())

        # data_obj = {
        #     "name": "Chardonnay",
        #     "description": "Goes with fish"
        # }
        # client.data_object.create(data_obj, "Wine")

        # self.client = chromadb.PersistentClient(path='temp/chromadb')
        # self.collection = self.client.get_or_create_collection(
        #     name='Embedia', metadata={"hnsw:space": "l2"})

    async def _insert(self, data: VectorDBInsert):
        pass
        # if not data.meta:
        #     data.meta = {}
        # self.collection.upsert(metadatas=[data.meta], embeddings=[data.embedding],
        #                        documents=[data.text], ids=[data.id])

    async def _get_similar(self, data: VectorDBGetSimilar):
        pass
        # resp = self.collection.query(query_embeddings=[data.embedding], n_results=data.n_results,
        #                              include=["metadatas", "documents", "distances"])
        # result = []
        # for i in range(len(resp["ids"][0])):
        #     doc = TextDoc(id=resp["ids"][0][i], contents=resp["documents"][0][i],
        #                   meta=resp["metadatas"][0][i])
        #     similarity = 1 / (1 + resp["distances"][0][i])
        #     result.append((similarity, doc))
        # return result


class OpenAILLMOptional1(LLM):
    def __init__(self):
        super().__init__(max_input_tokens=4000)

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAILLMOptional2(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer())

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAILLMOptional3(LLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=2)

    async def _complete(self, prompt: str) -> str:
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAIChatLLMOptional1(ChatLLM):
    def __init__(self):
        super().__init__(max_input_tokens=4096)

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


class OpenAIChatLLMOptional2(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer())

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


class OpenAIChatLLMOptional3(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=2)

    async def _reply(self, prompt: str) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


class OpenAIChatLLMOptional4(ChatLLM):
    def __init__(self):
        super().__init__(tokenizer=OpenAITokenizer(),
                         max_input_tokens=4096)

    async def _reply(self) -> str:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[{'role': msg.role, 'content': msg.content} for msg in self.chat_history],
        )
        return completion.choices[0].message.content


class PrintToolBroken1(Tool):
    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Sleep Tool",
            desc="Sleeps for 1 second",
            args=[{'name': 'texts', 'desc': 'The text to be printed. Type: String'}]))

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return {'output': 'done', 'exit_code': 0}


class PrintToolBroken2(Tool):
    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Sleep Tool",
            desc="Sleeps for 1 second",
            args=[ArgDocumentation(name="text", desc="The text to be printed. Type: String")]))

    async def _run(self, text: str):
        await self.human_confirmation(details={'text': text})
        print(text)
        return 'done'
