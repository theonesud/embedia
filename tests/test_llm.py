import pytest
import openai
from embedia.llm import LLM
from embedia.prompt import Prompt
from dotenv import load_dotenv
import os
load_dotenv()

PANDAS_EXPERT_LLM = """You are an expert in writing commands for the python pandas library.
Write a one-line command to solve the following problem: {query}. Command:"""


class OpenAILLM(LLM):
    async def complete(self, prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        completion = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0,
        )
        return completion.choices[0].text


@pytest.mark.asyncio
async def test_pandas_llm():
    llm = OpenAILLM()

    prompt = Prompt(template=PANDAS_EXPERT_LLM, context={
                    'query': ('I want to extract all the pincodes in the column "address" '
                              'and create another column "pincode"')})

    message = await llm.complete(prompt.to_str())
    assert isinstance(message, str)
    assert len(message) > 0
    print(message)
