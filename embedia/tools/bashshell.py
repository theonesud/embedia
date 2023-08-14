from embedia.tool import Tool
from typing import Type
from embedia import Message, ChatLLM
import subprocess
import asyncio

SHELL_EXPERT_SYSTEM = """You are an expert in writing commands for the {executable} shell.
Write one-line commands with inbuilt libraries to answer the user's question.
Reply only with the command and nothing else."""


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


class BashShellChat(Tool):

    def __init__(self, chatllm: Type[ChatLLM],
                 executable='/bin/sh', timeout=60, human_verification=True):
        super().__init__(name="Bash LLM",
                         desc="Convert natural language input into bash commands and run it",
                         args={"question": "natural language question that can be answered by running a bash command"},
                         chatllm=chatllm)
        self.executable = executable
        self.timeout = timeout
        self.human_verification = human_verification

    async def _run(self, question: str):
        shell_expert = self.chatllm(
            system_prompt=SHELL_EXPERT_SYSTEM.format(executable=self.executable))
        command = await shell_expert(Message(role='user', content=question))
        command = command.content
        if self.human_verification:
            self.confirm_before_running(command=command)

        bash_shell = BashShell(executable=self.executable, timeout=self.timeout)
        out, exit_code = await bash_shell(command=command)

        return out, exit_code
