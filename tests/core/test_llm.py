import pytest
from tests.core.definitions import OpenAILLM, OpenAILLMBroken1, OpenAILLMBroken2, OpenAILLMBroken3, OpenAILLMBroken4, OpenAILLMBroken5
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
    with pytest.raises(DefinitionError) as e:
        await llm('')
    print(e)
    with pytest.raises(DefinitionError) as e:
        await llm(5)
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAILLMBroken1()
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAILLMBroken2()
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAILLMBroken3()
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAILLMBroken4()
    print(e)
    with pytest.raises(DefinitionError) as e:
        llm = OpenAILLMBroken5()
        await llm('The capital of France is')
    print(e)
    # check token length error
