import pytest

from tests.core.definitions import OpenAIChatLLM
from embedia import Agent, ChatLLM, Message, Tokenizer
from embedia.tools import (BashShell, BashShellChat, PythonShell,
                           PythonShellChat)


@pytest.mark.asyncio
async def test_agent():
    python_shell_chat = PythonShellChat(chatllm=OpenAIChatLLM)
    python_shell = PythonShell()
    bash_shell_chat = BashShellChat(chatllm=OpenAIChatLLM)
    # bash_shell = BashShell()
    agent = Agent(chatllm=OpenAIChatLLM, tools=[python_shell_chat])
    # print(agent.agent.chat_history)
    resp = await agent('How many lines of code are there in the ~/embedia?')
