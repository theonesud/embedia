import asyncio

import pytest

from embedia.tools import PythonInterpreter


@pytest.mark.asyncio
async def test_python_tool():

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

    assert isinstance(output.output, int)
    assert isinstance(output.exit_code, int)
    assert output.output > 0
    assert output.exit_code == 0


@pytest.mark.asyncio
async def test_python_tool_timeout():
    python_shell = PythonInterpreter()
    with pytest.raises(asyncio.TimeoutError):
        await python_shell('import time; time.sleep(10)', timeout=1)


@pytest.mark.asyncio
async def test_python_tool_incorrect_command():

    python_shell = PythonInterpreter()

    output = await python_shell('printsss("asdafas")')

    assert isinstance(output.output, str)
    assert isinstance(output.exit_code, int)
    assert len(output.output) > 0
    assert output.exit_code == 1
