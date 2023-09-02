from copy import deepcopy
from typing import List

from embedia.core.chatllm import ChatLLM
from embedia.schema.persona import Persona
from embedia.utils.typechecking import check_min_val, check_type


def _init_check(question: str, personas: List[Persona], chatllm: ChatLLM, rounds: int):
    check_type(question, str, panel_discussion, 'question')
    for persona in personas:
        check_type(persona, str, panel_discussion, 'persona')
    check_type(chatllm, ChatLLM, panel_discussion, 'chatllm')
    check_type(rounds, int, panel_discussion, 'rounds')
    check_min_val(rounds, 1, 'rounds')


async def panel_discussion(question: str, personas: List[Persona], chatllm: ChatLLM, rounds: int = 5) -> None:
    _init_check(question, personas, chatllm, rounds)

    summarizer = deepcopy(chatllm)
    await summarizer.set_system_prompt(Persona.Summary)

    asker = deepcopy(chatllm)
    await asker.set_system_prompt(Persona.QuestionAsker)

    panelists = []
    for persona in personas:
        persona_chat = deepcopy(chatllm)
        await persona_chat.set_system_prompt(persona)
        panelists.append(persona_chat)

    old_buffer = question
    for i in range(rounds):
        current_buffer = []
        for panelist in panelists:
            current_buffer.append(await panelist(old_buffer))
        if i != rounds - 1:
            summary = await summarizer('\n'.join(current_buffer))
            old_buffer = await asker(summary)
