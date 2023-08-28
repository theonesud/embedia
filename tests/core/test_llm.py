import pytest
from tests.definitions import OpenAILLM
from embedia.utils.exceptions import DefinitionError


@pytest.mark.asyncio
async def test_llm():
    llm = OpenAILLM()
    message = await llm('The capital of France is')
    assert isinstance(message, str)
    assert len(message) > 0


@pytest.mark.asyncio
async def test_llm_error():
    llm = OpenAILLM()
    with pytest.raises(DefinitionError):
        await llm('')
    with pytest.raises(DefinitionError):
        await llm(5)
