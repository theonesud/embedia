import tiktoken
from dotenv import load_dotenv
import os
import openai
from embedia import LLM, ChatLLM, Message, Tokenizer
load_dotenv()


class OpenAIChatLLM(ChatLLM):
    async def _reply(self, message: Message) -> Message:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


class OpenAITokenizer(Tokenizer):
    async def _tokenize(self, text):
        return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)


class OpenAILLM(LLM):
    async def _complete(self, prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


# class EmptyOpenAIChatLLM(ChatLLM):
#     pass


# class WithoutMessageOpenAIChatLLM(ChatLLM):
#     async def _reply(self) -> Message:
#         openai.api_key = os.getenv("OPENAI_API_KEY")
#         completion = await openai.ChatCompletion.acreate(
#             model="gpt-3.5-turbo",
#             temperature=0.1,
#             max_tokens=500,
#             messages=[message.to_json() for message in self.chat_history],
#         )
#         return Message(**completion.choices[0].message)


# class ExtraArgsOpenAIChatLLM(ChatLLM):
#     async def _reply(self, message: Message, bs: str) -> Message:
#         openai.api_key = os.getenv("OPENAI_API_KEY")
#         completion = await openai.ChatCompletion.acreate(
#             model="gpt-3.5-turbo",
#             temperature=0.1,
#             max_tokens=500,
#             messages=[message.to_json() for message in self.chat_history],
#         )
#         return Message(**completion.choices[0].message)


class PassTool(Tool):
    def __init__(self):
        super().__init__(name="Pass Tool",
                         desc="Doesnt do anything")

    async def _run(self):
        return None, 0


class BashShell(Tool):
    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         args={"command": "The bash command to be run"})
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        self.confirm_before_running(command=command)
        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            return completed_process.stderr, 1
        else:
            return completed_process.stdout, 0


class IncorrectDocstingBashShell(Tool):
    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         args={"query": "The bash command to be run"})
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        self.confirm_before_running(command=command)
        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            return completed_process.stderr, 1
        else:
            return completed_process.stdout, 0


class IncorrectLLMBashShell(Tool):

    def __init__(self, chatllm: Optional[Type[ChatLLM]] = None, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         args={"command": "The bash command to be run"},
                         chatllm=chatllm)
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        if self.chatllm:
            shell_expert = self.chatllm(
                system_prompt=SHELL_EXPERT_SYSTEM.format(executable=self.executable))
            command = await shell_expert(Message(role='user', content=command))
            command = command.content

        self.confirm_before_running(command=command)

        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            return completed_process.stderr, 1
        else:
            return completed_process.stdout, 0


class GPTTokenizer(Tokenizer):
    async def _tokenize(self, text):
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return enc.encode(text, allowed_special=set(),
                          disallowed_special='all')


class OpenAIEmbedding(EmbeddingModel):
    def __init__(self):
        super().__init__(max_input_tokens=8191,
                         tokenizer=GPTTokenizer())

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
           retry=retry_if_not_exception_type(openai.InvalidRequestError))
    async def _embed(self, text: str):
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
