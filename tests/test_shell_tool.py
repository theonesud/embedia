import pytest
import openai
from embedia import ChatLLM, Message
from embedia.tools import BashShell, BashShellChat
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
