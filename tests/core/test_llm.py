import pytest

# from embedia.utils.exceptions import DefinitionError
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
    assert str(e) == "<ExceptionInfo ValueError('Length of input text: 5 token(s) is longer than max_input_tokens: 2') tblen=3>"
#     llm = OpenAILLM()
#     with pytest.raises(DefinitionError) as e:
#         await llm(5)
#     print(e)
#     with pytest.raises(DefinitionError) as e:
#         OpenAILLMBroken1()
#     print(e)
#     with pytest.raises(DefinitionError) as e:
#         OpenAILLMBroken2()
#     print(e)
#     with pytest.raises(DefinitionError) as e:
#         OpenAILLMBroken3()
#     print(e)
#     with pytest.raises(DefinitionError) as e:
#         OpenAILLMBroken4()
#     print(e)
#     with pytest.raises(DefinitionError) as e:
#         llm = OpenAILLMBroken5()
#         await llm('The capital of France is')
#     print(e)
    # check token length error
