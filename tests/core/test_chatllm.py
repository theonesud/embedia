import os
import pytest
from tests.definitions import OpenAIChatLLM, OpenAILLM, Message, ChatLLM
from embedia.utils.exceptions import DefinitionError
from embedia import Persona
os.makedirs('temp', exist_ok=True)


@pytest.mark.asyncio
async def test_chatllm():
    chatllm = OpenAIChatLLM()
    await chatllm.set_system_prompt(Persona.LibraryExpert.value.format(
        language='python', library='pandas'))

    await chatllm.save_chat('temp/openai_chatllm.pkl')
    await chatllm.load_chat('temp/openai_chatllm.pkl')

    reply = await chatllm(Message(role='user', content=('How to merge two dataframes?')))
    assert isinstance(reply, Message)
    assert len(reply.content) > 0


@pytest.mark.asyncio
async def test_from_llm():
    llm = OpenAILLM()
    chatllm = ChatLLM.from_llm(llm)
    await chatllm.set_system_prompt(Persona.LibraryExpert.value.format(
        language='python', library='pandas'))
    reply = await chatllm(Message(role='user', content=('How to merge two dataframes?')))
    assert isinstance(reply, Message)
    assert len(reply.content) > 0


@pytest.mark.asyncio
async def test_chatllm_error():
    chatllm = OpenAIChatLLM()
    with pytest.raises(DefinitionError):
        await chatllm(Message(role='user', content='How to merge two dataframes?'))
    await chatllm.set_system_prompt(Persona.LibraryExpert.value.format(
        language='python', library='pandas'))
    with pytest.raises(DefinitionError):
        await chatllm(Message(role='user', content=''))
    with pytest.raises(DefinitionError):
        await chatllm('How to merge two dataframes?')
