import asyncio
import subprocess

from embedia.core.tool import Tool
from embedia.schema.tool import (ParamDocumentation, ToolDocumentation,
                                 ToolReturn)


class Terminal(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Terminal",
            desc="Run the provided commands in the shell",
            params=[ParamDocumentation(
                name="command",
                desc="The terminal command to be run (type: str)"
            ), ParamDocumentation(
                name="executable",
                desc="The executable to run the command with (type: str). Defaults to /bin/sh"
            ), ParamDocumentation(
                name="timeout",
                desc="Timeout in seconds (type: int). Defaults to 60."
            )]))

    async def _run(self, command: str, executable='/bin/sh', timeout=60) -> ToolReturn:
        process = await asyncio.create_subprocess_shell(
            command, executable=executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            process.kill()
            raise
        if process.returncode != 0:
            return ToolReturn(output=stderr.decode(), exit_code=1)
        else:
            return ToolReturn(output=stdout.decode(), exit_code=0)
