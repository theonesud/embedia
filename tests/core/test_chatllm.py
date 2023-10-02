import os
import shutil

import pytest
from embedia import Persona

from tests.core.definitions import (
    ChatLLM,
    OpenAIChatLLM,
    OpenAIChatLLMOptional1,
    OpenAIChatLLMOptional2,
    OpenAIChatLLMOptional3,
    OpenAIChatLLMOptional4,
    OpenAIChatLLMBroken,
    OpenAILLM,
)


@pytest.mark.asyncio
async def test_chatllm():
    chatllm = OpenAIChatLLM()
    await chatllm.set_system_prompt(
        Persona.LibraryExpert.format(language="python", library="pandas")
    )

    shutil.rmtree("temp", ignore_errors=True)
    os.makedirs("temp")
    await chatllm.save_chat("temp/openai_chatllm.pkl")
    await chatllm.load_chat("temp/openai_chatllm.pkl")
    assert os.path.exists("temp/openai_chatllm.pkl")
    shutil.rmtree("temp")

    reply = await chatllm("How to merge two dataframes?")
    assert isinstance(reply, str)
    assert len(reply) > 0


@pytest.mark.asyncio
async def test_from_llm():
    llm = OpenAILLM()
    chatllm = ChatLLM.from_llm(llm)
    await chatllm.set_system_prompt(
        Persona.LibraryExpert.format(language="python", library="pandas")
    )
    reply = await chatllm("How to merge two dataframes?")
    assert isinstance(reply, str)
    assert len(reply) > 0


@pytest.mark.asyncio
async def test_chatllm_error():
    chatllm = OpenAIChatLLMOptional1()
    reply = await chatllm("How to merge two dataframes?")
    assert isinstance(reply, str)
    assert len(reply) > 0

    chatllm = OpenAIChatLLMOptional2()
    await chatllm.set_system_prompt(
        Persona.LibraryExpert.format(language="python", library="pandas")
    )
    reply = await chatllm("How to merge two dataframes?")
    assert isinstance(reply, str)
    assert len(reply) > 0

    chatllm = OpenAIChatLLMOptional3()
    with pytest.raises(ValueError) as e:
        await chatllm("How to merge two dataframes?")
    assert "Length of input text: 7 token(s) is longer than max_input_tokens: 2" in str(
        e
    )

    chatllm = OpenAIChatLLMOptional4()
    await chatllm.set_system_prompt(
        Persona.LibraryExpert.format(language="python", library="pandas")
    )
    reply = await chatllm("How to merge two dataframes?")
    assert isinstance(reply, str)
    assert len(reply) > 0

    chatllm = OpenAIChatLLMBroken()
    with pytest.raises(NotImplementedError) as e:
        reply = await chatllm("How to merge two dataframes?")
    assert (
        "Please call `ChatLLM` init method from your subclass init method to initialize the chat history"
        in str(e)
    )
