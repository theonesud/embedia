
import pytest

from embedia.tools import Simplify


# Temporarily disabled to save tokens

# @pytest.mark.asyncio
# async def test_simplify():
#     simplify_expert = Simplify(OpenAIChatLLM)
#     with open("README.md") as f:
#         text = f.read()
#     simplified = await simplify_expert(text)
#     assert isinstance(simplified[0], str)
#     assert len(simplified[0]) > 0
