import pytest

from embedia import Persona, panel_discussion
from tests.core.definitions import OpenAIChatLLM


@pytest.mark.asyncio
async def test_panel():
    await panel_discussion('How can Quantum Mechanics and General Relativity be unified?',
                           [Persona.SubjectExpert.format(subject='Quantum Mechanics'),
                            Persona.SubjectExpert.format(subject='General Relativity')], OpenAIChatLLM(), rounds=2)
