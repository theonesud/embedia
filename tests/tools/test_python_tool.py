import asyncio

import pytest

from embedia.tools import PythonInterpreter


@pytest.mark.asyncio
async def test_python_tool_without_llm():

    python_shell = PythonInterpreter()
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
async def test_python_tool_timeout():
    python_shell = PythonInterpreter(timeout=1)
    with pytest.raises(asyncio.TimeoutError):
        await python_shell('import time; time.sleep(10)')


@pytest.mark.asyncio
async def test_python_tool_incorrect_command():

    python_shell = PythonInterpreter()

    output = await python_shell('printsss("asdafas")')

    assert isinstance(output[0], str)
    assert isinstance(output[1], int)
    assert len(output[0]) > 0
    assert output[1] == 1
