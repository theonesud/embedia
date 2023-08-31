import asyncio
import subprocess

from embedia.core.tool import Tool


class Terminal(Tool):

    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(name="Terminal",
                         desc=f"Run the provided commands in the {executable} shell",
                         args={"command": "The terminal command to be run (type: str)"})
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        process = await asyncio.create_subprocess_shell(
            command, executable=self.executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout)
        except asyncio.TimeoutError:
            process.kill()
            raise
        if process.returncode != 0:
            return stderr.decode(), 1
        else:
            return stdout.decode(), 0
