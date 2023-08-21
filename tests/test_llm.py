import pytest
from dotenv import load_dotenv

from tests.utils import OpenAILLM, OpenAITokenizer

load_dotenv()

PANDAS_EXPERT_LLM = """You are an expert in writing commands for the python pandas library.
Write commands to solve the following problem: {query}. Command:"""


@pytest.mark.asyncio
async def test_pandas_llm():
    llm = OpenAILLM(OpenAITokenizer(), 4000)
    prompt = PANDAS_EXPERT_LLM.format(
        query=('I want to extract all the pincodes in the '
               'column "address" and create another column "pincode"'))
    message = await llm(prompt)
    assert isinstance(message, str)
    assert len(message) > 0
