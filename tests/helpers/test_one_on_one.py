
import pytest

from embedia import Persona, one_on_one_chat
from tests.core.definitions import OpenAIChatLLMCreative


@pytest.mark.asyncio
async def test_panel_2():
    await one_on_one_chat('Who am I?',
                          [Persona.AIPhilosopher, Persona.Buddha],
                          OpenAIChatLLMCreative(), rounds=2)
