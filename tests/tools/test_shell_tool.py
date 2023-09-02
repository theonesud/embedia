import asyncio

import pytest
from dotenv import load_dotenv

from embedia.tools import Terminal

load_dotenv()


@pytest.mark.asyncio
async def test_bash_tool_without_llm():

    bash_shell = Terminal(timeout=5)
    output = await bash_shell('ls -l')

    assert isinstance(output.output, str)
    assert isinstance(output.exit_code, int)
    assert len(output.output) > 0
    assert output.exit_code == 0


@pytest.mark.asyncio
async def test_bash_tool_timeout():

    bash_shell = Terminal(timeout=1)

    with pytest.raises(asyncio.TimeoutError):
        await bash_shell('sleep 10')


@pytest.mark.asyncio
async def test_bash_tool_incorrect_command():

    bash_shell = Terminal(timeout=1)

    output = await bash_shell('asdwadawdd')

    assert isinstance(output.output, str)
    assert isinstance(output.exit_code, int)
    assert len(output.output) > 0
    assert output.exit_code == 1


@pytest.mark.asyncio
async def test_bash_tool_different_shell():

    bash_shell = Terminal(timeout=5, executable='/bin/bash')

    output = await bash_shell('ps -p $$')

    assert isinstance(output.output, str)
    assert isinstance(output.exit_code, int)
    assert len(output.output) > 0
    assert output.exit_code == 0
