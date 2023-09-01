import asyncio
import subprocess

from embedia.core.tool import Tool
from embedia.schema.tool import ToolReturn, ArgDocumentation, ToolDocumentation


class Terminal(Tool):

    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(docs=ToolDocumentation(
            name="Terminal",
            desc=f"Run the provided commands in the {executable} shell",
            args=[ArgDocumentation(
                name="command",
                desc="The terminal command to be run (type: str)"
            )]))
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str) -> ToolReturn:
        process = await asyncio.create_subprocess_shell(
            command, executable=self.executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout)
        except asyncio.TimeoutError:
            process.kill()
            raise
        if process.returncode != 0:
            return ToolReturn(output=stderr.decode(), exit_code=1)
        else:
            return ToolReturn(output=stdout.decode(), exit_code=0)
