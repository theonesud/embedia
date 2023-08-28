import asyncio

import pytest
from dotenv import load_dotenv

from tests.definitions import OpenAIChatLLM
from embedia.tools import BashShell, BashShellChat

load_dotenv()


@pytest.mark.asyncio
async def test_bash_tool_without_llm():

    bash_shell = BashShell(timeout=5)
    output = await bash_shell('ls -l')

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert len(output[0]) > 0
    assert output[1] == 0


@pytest.mark.asyncio
async def test_bash_tool_with_llm(monkeypatch):

    monkeypatch.setattr('builtins.input', lambda _: 'y')

    bash_shell = BashShellChat(chatllm=OpenAIChatLLM)

    output = await bash_shell('List all files in this directory')

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert len(output[0]) > 0
    assert output[1] == 0


@pytest.mark.asyncio
async def test_bash_tool_with_llm_without_verification():

    bash_shell = BashShellChat(chatllm=OpenAIChatLLM, human_verification=False)

    output = await bash_shell('List all files in this directory')

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert len(output[0]) > 0
    assert output[1] == 0


@pytest.mark.asyncio
async def test_bash_tool_timeout():

    bash_shell = BashShell(timeout=1)

    with pytest.raises(asyncio.TimeoutError):
        await bash_shell('sleep 10')


@pytest.mark.asyncio
async def test_bash_tool_incorrect_command():

    bash_shell = BashShell(timeout=1)

    output = await bash_shell('asdwadawdd')

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert len(output[0]) > 0
    assert output[1] == 1


@pytest.mark.asyncio
async def test_bash_tool_different_shell():

    bash_shell = BashShell(timeout=5, executable='/bin/bash')

    output = await bash_shell('ps -p $$')

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert len(output[0]) > 0
    assert output[1] == 0
