import asyncio
import subprocess

from embedia.core.tool import Tool

# SHELL_EXPERT_SYSTEM = """You are an expert in writing commands for the {executable} shell.
# Write one-line commands with inbuilt libraries to answer the user's question.
# Reply only with the command and nothing else."""


class BashShell(Tool):

    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         args={"command": "The bash command to be run"})
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
