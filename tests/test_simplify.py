from embedia.tools import Simplify
import pytest
import openai
from embedia import ChatLLM, Message
from dotenv import load_dotenv
import os
load_dotenv()


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


# Temporarily disabled to save tokens

# @pytest.mark.asyncio
# async def test_simplify():
#     simplify_expert = Simplify(OpenAIChatLLM)
#     with open("README.md") as f:
#         text = f.read()
#     simplified = await simplify_expert(text)
#     assert isinstance(simplified[0], str)
#     assert len(simplified[0]) > 0
