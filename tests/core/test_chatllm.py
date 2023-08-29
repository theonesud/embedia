import os
import pytest
from tests.core.definitions import OpenAIChatLLM, OpenAILLM, ChatLLM, OpenAIChatLLMBroken1, OpenAIChatLLMBroken2, OpenAIChatLLMBroken3, OpenAIChatLLMBroken4, OpenAIChatLLMBroken5
from embedia.utils.exceptions import DefinitionError
from embedia import Persona
os.makedirs('temp', exist_ok=True)


@pytest.mark.asyncio
async def test_chatllm():
    chatllm = OpenAIChatLLM()
    await chatllm.set_system_prompt(Persona.LibraryExpert.format(
        language='python', library='pandas'))

    await chatllm.save_chat('temp/openai_chatllm.pkl')
    await chatllm.load_chat('temp/openai_chatllm.pkl')

    reply = await chatllm('How to merge two dataframes?')
    assert isinstance(reply, str)
    assert len(reply.content) > 0


@pytest.mark.asyncio
async def test_from_llm():
    llm = OpenAILLM()
    chatllm = ChatLLM.from_llm(llm)
    await chatllm.set_system_prompt(Persona.LibraryExpert.format(
        language='python', library='pandas'))
    reply = await chatllm('How to merge two dataframes?')
    assert isinstance(reply, str)
    assert len(reply.content) > 0


@pytest.mark.asyncio
async def test_chatllm_error():
    chatllm = OpenAIChatLLM()
    with pytest.raises(DefinitionError) as e:
        await chatllm('How to merge two dataframes?')
    print(e)
    await chatllm.set_system_prompt(Persona.LibraryExpert.format(
        language='python', library='pandas'))
    with pytest.raises(DefinitionError) as e:
        await chatllm('')
    print(e)
    with pytest.raises(DefinitionError) as e:
        await chatllm(666)
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAIChatLLMBroken1()
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAIChatLLMBroken2()
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAIChatLLMBroken3()
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAIChatLLMBroken4()
    print(e)
    with pytest.raises(DefinitionError) as e:
        chatllm = OpenAIChatLLMBroken5()
        await chatllm.set_system_prompt(Persona.LibraryExpert.format(
            language='python', library='pandas'))
        await chatllm('How to merge two dataframes?')
    print(e)
    with pytest.raises(DefinitionError) as e:
        # check token length
        pass
