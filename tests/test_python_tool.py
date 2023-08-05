import pytest
import openai
from embedia.chatllm import ChatLLM
from embedia.message import Message
from embedia.tools.pythonshell import PythonShell
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()


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
async def test_python_tool_without_llm():

    python_shell = PythonShell()
    output = await python_shell.run('print(x+y+5)', globals={'x': 5}, locals={'y': 10})
    print(output[0])

    assert isinstance(output[0], str)
    assert isinstance(output[1], str)
    assert int(output[0]) == 20
    assert len(output[1]) == 0


@pytest.mark.asyncio
async def test_python_tool_with_llm(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')

    python_shell = PythonShell(chatllm=OpenAIChatLLM)
    output = await python_shell.run('Print the result of adding x, y and 5', globals={'x': 5}, locals={'y': 10})
    print(output[0])

    assert isinstance(output[0], str)
    assert isinstance(output[1], str)
    assert int(output[0]) == 20
    assert len(output[1]) == 0


@pytest.mark.asyncio
async def test_python_tool_with_llm_without_verification():

    python_shell = PythonShell(chatllm=OpenAIChatLLM, human_verification=False)

    output = await python_shell.run('Print the result of adding x, y and 5', globals={'x': 5}, locals={'y': 10})
    print(output[0])

    assert isinstance(output[0], str)
    assert len(output[0]) > 0
    assert isinstance(output[1], str)
    assert len(output[1]) == 0


@pytest.mark.asyncio
async def test_python_tool_timeout():
    python_shell = PythonShell(timeout=1)
    with pytest.raises(asyncio.TimeoutError):
        await python_shell.run('import time; time.sleep(10)')


@pytest.mark.asyncio
async def test_python_tool_incorrect_command():

    python_shell = PythonShell()

    output = await python_shell.run('printsss("Yo")')
    print(output[1])

    assert isinstance(output[0], str)
    assert isinstance(output[1], str)
    assert len(output[0]) == 0
    assert len(output[1]) > 0
