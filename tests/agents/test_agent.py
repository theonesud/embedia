import pytest

from embedia.agents import ToolUser
from embedia.tools import (PythonInterpreter, Terminal)
from tests.core.definitions import OpenAIChatLLM


@pytest.mark.asyncio
async def test_tool_user():
    tool_user = ToolUser(chatllm=OpenAIChatLLM, tools=[PythonInterpreter(), Terminal()])
    # print(tool_user.tool_user.chat_history)
    # resp = await tool_user('How many lines of code are there in the ~/embedia?')
    resp = await tool_user('Run the following command: ls -l')
    print(resp)
