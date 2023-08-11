import pytest
import openai
from embedia.chatllm import ChatLLM
from embedia.message import Message
from embedia.tools.pythonshell import PythonShell, PythonShellChat
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()


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


# TODO: Write one test for single line and another for multiline commands

@pytest.mark.asyncio
async def test_python_tool_without_llm():

    python_shell = PythonShell()
    output = await python_shell('import os\n\ndef count_lines_of_code(directory):\n    total_lines = 0\n    for root, dirs, files in os.walk(directory):\n        for file in files:\n            if file.endswith(".py"):\n                file_path = os.path.join(root, file)\n                with open(file_path, "r") as f:\n                    lines = f.readlines()\n                    total_lines += len(lines)\n    return total_lines\n\ncurrent_directory = os.getcwd()\ncount_lines_of_code(current_directory)')
    print(output)

    # assert isinstance(output[0], str)
    # assert isinstance(output[1], str)
    # assert int(output[0]) == 20
    # assert len(output[1]) == 0


@pytest.mark.asyncio
async def test_python_tool_with_llm(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')

    python_shell = PythonShellChat(chatllm=OpenAIChatLLM)
    output = await python_shell('Print the result of adding x, y and 5',
                                global_vars={'x': 5}, local_vars={'y': 10})
    print(output[0])

    assert isinstance(output[0], str)
    assert isinstance(output[1], str)
    assert int(output[0]) == 20
    assert len(output[1]) == 0


@pytest.mark.asyncio
async def test_python_tool_with_llm_without_verification():

    python_shell = PythonShellChat(chatllm=OpenAIChatLLM, human_verification=False)

    output = await python_shell('Print the result of adding x, y and 5',
                                global_vars={'x': 5}, local_vars={'y': 10})
    print(output[0])

    assert isinstance(output[0], str)
    assert len(output[0]) > 0
    assert isinstance(output[1], str)
    assert len(output[1]) == 0


@pytest.mark.asyncio
async def test_python_tool_timeout():
    python_shell = PythonShell(timeout=1)
    with pytest.raises(asyncio.TimeoutError):
        await python_shell('import time; time.sleep(10)')


@pytest.mark.asyncio
async def test_python_tool_incorrect_command():

    python_shell = PythonShell()

    output = await python_shell('printsss("Yo")')
    print(output[1])

    assert isinstance(output[0], str)
    assert isinstance(output[1], str)
    assert len(output[0]) == 0
    assert len(output[1]) > 0
