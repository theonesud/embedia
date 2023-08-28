from embedia.core.chatllm import ChatLLM
from embedia.schema.message import Message
from typing import List
from copy import deepcopy


async def panel_discussion(question: str, personas: List[str], chatllm: ChatLLM, rounds: int = 5):
    panelists = []
    for persona in personas:
        persona_llm = deepcopy(chatllm)
        persona_llm.set_system_prompt(persona)
        panelists.append(persona_llm)

    old_buffer = Message(role='user', content=question)
    for _ in range(rounds):
        current_buffer = []
        for panelist in panelists:
            current_buffer.append(await panelist(Message(role='user', content=old_buffer)))
        old_buffer = Message(role='user', content='\n'.join([message.content for message in current_buffer]))
