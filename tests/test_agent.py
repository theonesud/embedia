from embedia.tools.pythonshell import PythonShell, PythonShellChat
from embedia.tools.bashshell import BashShell, BashShellChat
from embedia.agent import Agent
from embedia.chatllm import ChatLLM
from embedia.message import Message
from dotenv import load_dotenv
import os
import openai
import asyncio
import pytest
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
async def test_agent():
    python_shell_chat = PythonShellChat(chatllm=OpenAIChatLLM)
    python_shell = PythonShell()
    bash_shell_chat = BashShellChat(chatllm=OpenAIChatLLM)
    # bash_shell = BashShell()
    agent = Agent(chatllm=OpenAIChatLLM, tools=[python_shell_chat])
    # print(agent.agent.chat_history)
    resp = await agent('How many lines of code are there in the current directory?')
    # print(resp)
