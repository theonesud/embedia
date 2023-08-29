from embedia.core.chatllm import ChatLLM
from typing import List
from copy import deepcopy
from embedia.schema.persona import Persona
from embedia.utils.typechecking import check_type, check_min_val


async def panel_discussion(question: str, personas: List[Persona], chatllm: ChatLLM, rounds: int = 5) -> None:
    check_type(question, str)
    for persona in personas:
        check_type(persona, str)
    check_type(chatllm, ChatLLM)
    check_type(rounds, int)
    check_min_val(rounds, 1)
    summarizer = deepcopy(chatllm)
    asker = deepcopy(chatllm)
    await summarizer.set_system_prompt(Persona.Summary)
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
            summary = await summarizer('\n'.join([message.content for message in current_buffer]))
            old_buffer = await asker(summary.content)
