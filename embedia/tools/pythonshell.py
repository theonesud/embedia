import ast
import asyncio
import multiprocessing as mp
from contextlib import redirect_stdout
from io import StringIO
from embedia.core.tool import Tool

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
