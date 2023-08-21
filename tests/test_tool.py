import os
import subprocess
from typing import Optional, Type

import openai
import pytest

from embedia import LLM, ChatLLM, Message, Tool
from embedia.core.tool import DeniedByUserException

SHELL_EXPERT_SYSTEM = """You are an expert in writing commands for the {executable} shell.
Write one-line commands with inbuilt libraries to solve the user's problems.
Reply only with the command and nothing else."""





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
