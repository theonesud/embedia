import pytest
import openai
from embedia.chatllm import ChatLLM
from embedia.message import Message
from embedia.tools.bashshell import BashShell
from dotenv import load_dotenv
import os
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
async def test_bash_tool_without_llm(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')

    bash_shell = BashShell()
    output = await bash_shell.run('ls -l')
    print(output)

    assert isinstance(output, str)
    assert len(output) > 0


@pytest.mark.asyncio
async def test_bash_tool_with_llm(monkeypatch):

    monkeypatch.setattr('builtins.input', lambda _: 'y')

    bash_shell = BashShell(chatllm=OpenAIChatLLM)

    output = await bash_shell.run('List all files in this directory')
    print(output)

    assert isinstance(output, str)
    assert len(output) > 0
