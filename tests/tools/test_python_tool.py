import asyncio
import pytest

from embedia.tools import PythonShell, PythonShellChat
from tests.definitions import OpenAIChatLLM


@pytest.mark.asyncio
async def test_python_tool_without_llm():

    python_shell = PythonShell()
    output = await python_shell("""import os

def count_lines_of_code(directory):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    total_lines += len(lines)
    return total_lines

current_directory = os.getcwd()
count_lines_of_code(current_directory)""")

    assert isinstance(output[0], int)
    assert isinstance(output[1], int)
    assert output[0] > 0
    assert output[1] == 0


@pytest.mark.asyncio
async def test_python_tool_with_llm(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')

    python_shell = PythonShellChat(chatllm=OpenAIChatLLM)
    output = await python_shell('Print the result of adding x, y and 5',
                                vars={'x': 5, 'y': 10})

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert int(output[0]) == 20
    assert output[1] == 0


@pytest.mark.asyncio
async def test_python_tool_with_llm_without_verification():

    python_shell = PythonShellChat(chatllm=OpenAIChatLLM, human_verification=False)

    output = await python_shell('Print the result of adding x, y and 5',
                                vars={'x': 5, 'y': 10})

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert int(output[0]) == 20
    assert output[1] == 0


@pytest.mark.asyncio
async def test_python_tool_timeout():
    python_shell = PythonShell(timeout=1)
    with pytest.raises(asyncio.TimeoutError):
        await python_shell('import time; time.sleep(10)')


@pytest.mark.asyncio
async def test_python_tool_incorrect_command():

    python_shell = PythonShell()

    output = await python_shell('printsss("asdafas")')

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert len(output[0]) > 0
    assert output[1] == 1
