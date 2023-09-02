import pytest

from tests.core.definitions import (OpenAILLM, OpenAILLMOptional1, OpenAILLMOptional2, OpenAILLMOptional3)


@pytest.mark.asyncio
async def test_llm():
    llm = OpenAILLM()
    message = await llm('The capital of France is')
    assert isinstance(message, str)
    assert len(message) > 0

    llm = OpenAILLMOptional1()
    message = await llm('The capital of France is')
    assert isinstance(message, str)
    assert len(message) > 0

    llm = OpenAILLMOptional2()
    message = await llm('The capital of France is')
    assert isinstance(message, str)
    assert len(message) > 0


@pytest.mark.asyncio
async def test_llm_error():
    llm = OpenAILLMOptional3()
    with pytest.raises(ValueError) as e:
        await llm('The capital of France is')
    assert 'Length of input text: 5 token(s) is longer than max_input_tokens: 2' in str(e)
