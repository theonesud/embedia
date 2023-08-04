from embedia.tool import Tool
from typing import Optional, Type
from embedia.message import Message
from embedia.chatllm import ChatLLM
import subprocess

SHELL_EXPERT_SYSTEM = """You are an expert in writing commands for the {executable} shell.
Write one-line commands with inbuilt libraries to solve the user's problems. Reply only with the command and nothing else."""


class BashShell(Tool):

    def __init__(self, chatllm: Optional[Type[ChatLLM]] = None, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         examples="ls -l, pwd",
                         args="command: str",
                         returns="output: str",
                         chatllm=chatllm)
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        if self.chatllm:
            shell_expert = self.chatllm(
                system_prompt=SHELL_EXPERT_SYSTEM.format(executable=self.executable))
            command = await shell_expert.reply(Message(role='user', content=command))
            command = command.content

        self.confirm_before_running(command=command)

        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            output = completed_process.stderr
        else:
            output = completed_process.stdout
        return output
