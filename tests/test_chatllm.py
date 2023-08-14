import pytest
import openai
from embedia import ChatLLM, Message, LLM
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
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


class WithoutMessageOpenAIChatLLM(ChatLLM):
    async def _reply(self) -> Message:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


class ExtraArgsOpenAIChatLLM(ChatLLM):
    async def _reply(self, message: Message, bs: str) -> Message:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=500,
            messages=[message.to_json() for message in self.chat_history],
        )
        return Message(**completion.choices[0].message)


class OpenAILLM(LLM):
    async def _complete(self, prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.1,
        )
        return completion.choices[0].text


@pytest.mark.asyncio
async def test_not_implemented_error_chatllm():
    openai_chatllm = EmptyOpenAIChatLLM(PANDAS_EXPERT_SYSTEM)
    with pytest.raises(NotImplementedError):
        await openai_chatllm(
            Message(role='user',
                    content=(
                        'I want to extract all the '
                        'pincodes in the column "address" and create '
                        'another column "pincode"')))


@pytest.mark.asyncio
async def test_pandas_chatllm():
    openai_chatllm = OpenAIChatLLM(PANDAS_EXPERT_SYSTEM)

    await openai_chatllm(
        Message(role='user',
                content=('I want to extract all the '
                         'pincodes in the column "address" and create '
                         'another column "pincode"')))

    await openai_chatllm(
        Message(role='user',
                content=('In the above command,'
                         'append "No" before each pincode')))

    openai_chatllm.save_chat('temp/openai_chatllm.pkl')
    openai_chatllm.load_chat('temp/openai_chatllm.pkl')

    for message in openai_chatllm.chat_history:
        assert isinstance(message, Message)
        assert message.role in ('assistant', 'user', 'system')
        assert len(message.content) > 0


@pytest.mark.asyncio
async def test_pandas_without_msg_chatllm():
    openai_chatllm = WithoutMessageOpenAIChatLLM(PANDAS_EXPERT_SYSTEM)

    with pytest.raises(ValueError):
        await openai_chatllm(
            Message(role='user',
                    content=('I want to extract all the '
                             'pincodes in the column "address" and create '
                             'another column "pincode"')))


@pytest.mark.asyncio
async def test_pandas_extra_args_chatllm():
    openai_chatllm = ExtraArgsOpenAIChatLLM(PANDAS_EXPERT_SYSTEM)

    with pytest.raises(ValueError):
        await openai_chatllm(
            Message(role='user',
                    content=('I want to extract all the '
                             'pincodes in the column "address" and create '
                             'another column "pincode"')))


@pytest.mark.asyncio
async def test_llm_to_chatllm():
    openai_llm = OpenAILLM()
    openai_chatllm = ChatLLM.from_llm(openai_llm, PANDAS_EXPERT_SYSTEM)

    await openai_chatllm(Message(
        role='user',
        content=('I want to extract all the pincodes '
                 'in the column "address" and create another column "pincode"')))

    await openai_chatllm(Message(role='user', content=('In the above command, append "No" '
                                                       'before each pincode')))

    openai_chatllm.save_chat('temp/openai_chatllm.pkl')
    openai_chatllm.load_chat('temp/openai_chatllm.pkl')

    for message in openai_chatllm.chat_history:
        assert isinstance(message, Message)
        assert message.role in ('assistant', 'user', 'system')
        assert len(message.content) > 0
