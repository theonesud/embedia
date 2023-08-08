import pytest
import openai
from embedia.chatllm import ChatLLM
from embedia.message import Message
from dotenv import load_dotenv
import os
load_dotenv()
os.makedirs('temp', exist_ok=True)

PANDAS_EXPERT_SYSTEM = """You are an expert in writing commands for the python pandas library.
Write one-line commands to solve the user's problems"""


class EmptyOpenAIChatLLM(ChatLLM):
    pass


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


class WithoutMessageOpenAIChatLLM(ChatLLM):
    async def _reply(self) -> Message:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


class ExtraArgsOpenAIChatLLM(ChatLLM):
    async def _reply(self, message: Message, bs: str) -> Message:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


@pytest.mark.asyncio
async def test_not_implemented_error_chatllm():
    openai_chatllm = EmptyOpenAIChatLLM(PANDAS_EXPERT_SYSTEM)
    with pytest.raises(NotImplementedError):
        await openai_chatllm.reply(Message(role='user', content='I want to extract all the \
                                           pincodes in the column "address" and create \
                                           another column "pincode"'))


@pytest.mark.asyncio
async def test_pandas_chatllm():
    openai_chatllm = OpenAIChatLLM(PANDAS_EXPERT_SYSTEM)

    await openai_chatllm.reply(Message(role='user', content='I want to extract all the \
                                       pincodes in the column "address" and create \
                                       another column "pincode"'))

    await openai_chatllm.reply(Message(role='user', content='In the above command,\
                                        append "No" before each pincode'))

    openai_chatllm.save_chat('temp/openai_chatllm.pkl')
    openai_chatllm.load_chat('temp/openai_chatllm.pkl')

    for message in openai_chatllm.chat_history:
        assert isinstance(message, Message)
        assert message.role in ('assistant', 'user', 'system')
        assert len(message.content) > 0
        print(message.role, ': ', message.content)


@pytest.mark.asyncio
async def test_pandas_without_msg_chatllm():
    openai_chatllm = WithoutMessageOpenAIChatLLM(PANDAS_EXPERT_SYSTEM)

    with pytest.raises(ValueError):
        await openai_chatllm.reply(Message(role='user', content='I want to extract all the\
                                            pincodes in the column "address" and create \
                                           another column "pincode"'))


@pytest.mark.asyncio
async def test_pandas_extra_args_chatllm():
    openai_chatllm = ExtraArgsOpenAIChatLLM(PANDAS_EXPERT_SYSTEM)

    with pytest.raises(ValueError):
        await openai_chatllm.reply(Message(role='user', content='I want to extract all the \
                                           pincodes in the column "address" and create \
                                           another column "pincode"'))
