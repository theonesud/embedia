from embedia.tool import DeniedByUserException
import pytest
from embedia.tool import Tool
from embedia.message import Message
from embedia.chatllm import ChatLLM
from embedia.llm import LLM
from typing import Optional, Type
import subprocess
import openai
import os

SHELL_EXPERT_SYSTEM = """You are an expert in writing commands for the {executable} shell.
Write one-line commands with inbuilt libraries to solve the user's problems. Reply only with the command and nothing else."""


class BashShell(Tool):
    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         examples="ls -l, pwd",
                         args="command: str",
                         returns="output: str")
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        self.confirm_before_running(command=command)
        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            output = completed_process.stderr
        else:
            output = completed_process.stdout
        return output


class IncorrectDocstingBashShell(Tool):
    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         examples="ls -l, pwd",
                         args="query: str",
                         returns="output: str")
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        self.confirm_before_running(command=command)
        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            output = completed_process.stderr
        else:
            output = completed_process.stdout
        return output


class IncorrectLLMBashShell(Tool):

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


class OpenAILLM(LLM):
    async def complete(self, prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0,
        )
        return completion.choices[0].text


class OpenAIChatLLM(ChatLLM):
    async def _reply(self, message: Message) -> Message:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


@pytest.mark.asyncio
async def test_user_denied(monkeypatch):

    monkeypatch.setattr('builtins.input', lambda _: 'n')

    bash_shell = BashShell()
    with pytest.raises(DeniedByUserException):
        await bash_shell.run('ls -l')


@pytest.mark.asyncio
async def test_incorrect_docsting():

    bash_shell = IncorrectDocstingBashShell()
    with pytest.raises(ValueError):
        await bash_shell.run('ls -l')


@pytest.mark.asyncio
async def test_incorrect_llm():

    with pytest.raises(TypeError):
        IncorrectLLMBashShell(chatllm=OpenAILLM)

    with pytest.raises(TypeError):
        IncorrectLLMBashShell(chatllm=OpenAIChatLLM())
