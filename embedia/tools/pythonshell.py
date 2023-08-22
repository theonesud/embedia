import ast
import asyncio
import multiprocessing as mp
from contextlib import redirect_stdout
from io import StringIO
from typing import Type

from embedia.core.chatllm import ChatLLM
from embedia.core.tool import Tool
from embedia.schema.message import Message

# PYTHON_EXPERT_SYSTEM = """You are an expert python programmer.
# Write python code to answer the user's question.
# Reply only with the code and nothing else."""

# make the timeout and background process a tool function


class PythonShell(Tool):

    def __init__(self, timeout=60):
        super().__init__(name="Python Shell",
                         desc="Run valid python code",
                         args={"code": "Valid python code to be run by a python interpreter",
                               "vars": "A python dictionary containing variables to be passed to the code"})
        self.timeout = timeout

    def _target_func(self, queue, code, vars):
        try:
            global_vars = {'__builtins__': __builtins__}
            local_vars = vars
            tree = ast.parse(code)
            imports = [x for x in tree.body if isinstance(x, ast.Import)]
            imports_from = [x for x in tree.body if isinstance(x, ast.ImportFrom)]
            for import_ in imports:
                global_vars.update({import_.names[0].name: __import__(import_.names[0].name)})
            for import_from in imports_from:
                for name in import_from.names:
                    global_vars.update(
                        {name.name: getattr(__import__(import_from.module), name.name)})
            module = ast.Module(tree.body[:-1], type_ignores=[])
            exec(ast.unparse(module), global_vars, local_vars)
            module_end = ast.Module(tree.body[-1:], type_ignores=[])
            module_end_str = ast.unparse(module_end)
            io_buffer = StringIO()
            try:
                with redirect_stdout(io_buffer):
                    ret = eval(module_end_str, global_vars, local_vars)
                    if ret is None:
                        output = io_buffer.getvalue()
                    else:
                        output = ret
            except Exception:
                with redirect_stdout(io_buffer):
                    exec(module_end_str, global_vars, local_vars)
                output = io_buffer.getvalue()
            queue.put([output, 0])
        except Exception as e:
            queue.put([str(e), 1])

    async def _run(self, code: str, vars: dict = {}):
        loop = asyncio.get_running_loop()
        queue = mp.Queue()
        process = mp.Process(target=self._target_func, args=(queue, code, vars))
        process.start()
        process.join(self.timeout)
        if process.is_alive():
            process.kill()
            raise asyncio.TimeoutError
        result = await loop.run_in_executor(None, queue.get)
        return result[0], result[1]


# class PythonShellChat(Tool):
#     def __init__(self, chatllm: Type[ChatLLM],
#                  timeout=60, human_verification=True):
#         super().__init__(name="Python LLM",
#                          desc="Convert natural language input to python code and run it",
#                          args={"question": "natural language question that can be answered by running python code",
#                                "vars": "A python dictionary containing variables to be passed to the code"},
#                          chatllm=chatllm)
#         self.timeout = timeout
#         self.human_verification = human_verification

#     async def _run(self, question: str, vars: dict = {}):

#         python_expert = self.chatllm(system_prompt=PYTHON_EXPERT_SYSTEM)
#         prompt = (f"question: {question}, variables available: {vars}")
#         code = await python_expert(Message(role='user', content=prompt))
#         code = code.content

#         if self.human_verification:
#             self.confirm_before_running(code=code, vars=vars)

#         python_shell = PythonShell(timeout=self.timeout)
#         output, exit_code = await python_shell(code=code, vars=vars)

#         return output, exit_code
