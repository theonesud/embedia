from embedia.tool import DeniedByUserException
import pytest
from embedia import Tool, Message, ChatLLM, LLM
from typing import Optional, Type
import subprocess
import openai
import os

SHELL_EXPERT_SYSTEM = """You are an expert in writing commands for the {executable} shell.
Write one-line commands with inbuilt libraries to solve the user's problems.
Reply only with the command and nothing else."""


class PassTool(Tool):
    def __init__(self):
        super().__init__(name="Pass Tool",
                         desc="Doesnt do anything")

    async def _run(self):
        return None, 0


class BashShell(Tool):
    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         args={"command": "The bash command to be run"})
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        self.confirm_before_running(command=command)
        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            return completed_process.stderr, 1
        else:
            return completed_process.stdout, 0


class IncorrectDocstingBashShell(Tool):
    def __init__(self, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         args={"query": "The bash command to be run"})
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        self.confirm_before_running(command=command)
        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            return completed_process.stderr, 1
        else:
            return completed_process.stdout, 0


class IncorrectLLMBashShell(Tool):

    def __init__(self, chatllm: Optional[Type[ChatLLM]] = None, executable='/bin/sh', timeout=60):
        super().__init__(name="Bash Shell",
                         desc="Run bash commands",
                         args={"command": "The bash command to be run"},
                         chatllm=chatllm)
        self.executable = executable
        self.timeout = timeout

    async def _run(self, command: str):
        if self.chatllm:
            shell_expert = self.chatllm(
                system_prompt=SHELL_EXPERT_SYSTEM.format(executable=self.executable))
            command = await shell_expert(Message(role='user', content=command))
            command = command.content

        self.confirm_before_running(command=command)

        completed_process = subprocess.run(
            command, executable=self.executable, shell=True, capture_output=True,
            text=True, timeout=self.timeout)
        if completed_process.returncode != 0:
            return completed_process.stderr, 1
        else:
            return completed_process.stdout, 0


class OpenAILLM(LLM):
    async def _complete(self, prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


class OpenAIChatLLM(ChatLLM):
    async def _reply(self, message: Message) -> Message:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


@pytest.mark.asyncio
async def test_user_denied(monkeypatch):

    monkeypatch.setattr('builtins.input', lambda _: 'n')

    bash_shell = BashShell()
    with pytest.raises(DeniedByUserException):
        await bash_shell('ls -l')


@pytest.mark.asyncio
async def test_incorrect_docsting():

    bash_shell = IncorrectDocstingBashShell()
    with pytest.raises(ValueError):
        await bash_shell('ls -l')


@pytest.mark.asyncio
async def test_incorrect_llm():

    with pytest.raises(TypeError):
        IncorrectLLMBashShell(chatllm=OpenAILLM)

    with pytest.raises(TypeError):
        IncorrectLLMBashShell(chatllm=OpenAIChatLLM())


@pytest.mark.asyncio
async def test_pass_tool():

    passtool = PassTool()
    await passtool()
