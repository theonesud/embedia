import pytest
import openai
from embedia.llm import LLM
from embedia.chatllm import ChatLLM
from embedia.message import Message
from dotenv import load_dotenv
import os
load_dotenv()

PANDAS_EXPERT_SYSTEM = """You are an expert in writing commands for the python pandas library.
Write one-line commands to solve the user's problems"""


class OpenAILLM(LLM):
    async def complete(self, prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0,
        )
        return completion.choices[0].text


@pytest.mark.asyncio
async def test_llm_to_chatllm():
    openai_llm = OpenAILLM()
    openai_chatllm = ChatLLM.from_llm(openai_llm, PANDAS_EXPERT_SYSTEM)

    await openai_chatllm.reply(Message(role='user', content='I want to extract all the pincodes in the column "address" and create another column "pincode"'))

    await openai_chatllm.reply(Message(role='user', content='In the above command, append "No" before each pincode'))

    openai_chatllm.save_chat('tests/openai_chatllm.pkl')
    openai_chatllm.load_chat('tests/openai_chatllm.pkl')

    for message in openai_chatllm.chat_history:
        assert isinstance(message, Message)
        assert message.role in ('assistant', 'user', 'system')
        assert len(message.content) > 0
        print(message.role, ': ', message.content)
