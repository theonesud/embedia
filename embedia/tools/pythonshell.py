import multiprocessing as mp
from embedia.tool import Tool
from typing import Optional, Type
from embedia.message import Message
from embedia.chatllm import ChatLLM
import asyncio
from io import StringIO
import sys

PYTHON_EXPERT_SYSTEM = """You are an expert in writing python code.
Write one-line commands with inbuilt libraries to solve the user's problems. Reply only with the command and nothing else."""


class PythonShell(Tool):

    def __init__(self, chatllm: Optional[Type[ChatLLM]] = None,
                 timeout=60, human_verification=True):
        super().__init__(name="Python Shell",
                         desc="Run python commands",
                         examples="print('Hello World!'), 2+2",
                         args="command: str, globals: dict, locals: dict",
                         returns="output: str",
                         chatllm=chatllm)
        self.timeout = timeout
        self.human_verification = human_verification

    async def _run(self, command: str, globals: dict = {}, locals: dict = {}):
        if self.chatllm:
            python_expert = self.chatllm(system_prompt=PYTHON_EXPERT_SYSTEM)
            prompt = f"query: {command}, global variables available: {globals}, local variables available: {locals}"
            command = await python_expert.reply(Message(role='user', content=prompt))
            command = command.content

            if self.human_verification:
                self.confirm_before_running(command=command, globals=globals, locals=locals)

        def target_func(queue):
            try:
                stdout = sys.stdout
                sys.stdout = StringIO()
                exec(command, globals, locals)
                output = sys.stdout.getvalue()
                sys.stdout = stdout
                queue.put([output, ""])
            except Exception as e:
                queue.put(["", str(e)])

        loop = asyncio.get_running_loop()
        queue = mp.Queue()
        process = mp.Process(target=target_func, args=(queue,))
        process.start()
        process.join(self.timeout)
        if process.is_alive():
            process.kill()
            raise asyncio.TimeoutError
        result = await loop.run_in_executor(None, queue.get)
        return result[0], result[1]
