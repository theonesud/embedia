import asyncio

import pytest
from dotenv import load_dotenv

from embedia.tools import Terminal

load_dotenv()


@pytest.mark.asyncio
async def test_bash_tool():

    bash_shell = Terminal()
    output = await bash_shell('ls -l', timeout=5)

    assert isinstance(output.output, str)
    assert isinstance(output.exit_code, int)
    assert len(output.output) > 0
    assert output.exit_code == 0


@pytest.mark.asyncio
async def test_bash_tool_timeout():

    bash_shell = Terminal()

    with pytest.raises(asyncio.TimeoutError):
        await bash_shell('sleep 10', timeout=1)


@pytest.mark.asyncio
async def test_bash_tool_incorrect_command():

    bash_shell = Terminal()

    output = await bash_shell('asdwadawdd')

    assert isinstance(output.output, str)
    assert isinstance(output.exit_code, int)
    assert len(output.output) > 0
    assert output.exit_code == 1


@pytest.mark.asyncio
async def test_bash_tool_different_shell():

    bash_shell = Terminal()

    output = await bash_shell('ps -p $$', timeout=5, executable='/bin/bash')

    assert isinstance(output.output, str)
    assert isinstance(output.exit_code, int)
    assert len(output.output) > 0
    assert output.exit_code == 0
