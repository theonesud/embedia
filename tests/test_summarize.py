
import pytest

from embedia import ChatLLM, Message
from embedia.tools import Summarize


# Temporarily disabled to save tokens

# @pytest.mark.asyncio
# async def test_summarize():
#     summarize_expert = Summarize(OpenAIChatLLM)
#     with open("README.md") as f:
#         text = f.read()
#     summary = await summarize_expert(text)
#     assert isinstance(summary[0], str)
#     assert len(summary[0]) > 0
