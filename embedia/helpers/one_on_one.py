from copy import deepcopy
from typing import List

from embedia.core.chatllm import ChatLLM
from embedia.schema.persona import Persona
from embedia.utils.typechecking import (check_exact_val, check_min_val,
                                        check_type)


def _init_check(question: str, personas: List[Persona], chatllm: ChatLLM, rounds: int):
    check_type(question, str, one_on_one_chat, 'question')
    for persona in personas:
        check_type(persona, str, one_on_one_chat, 'persona')
    check_type(chatllm, ChatLLM, one_on_one_chat, 'chatllm')
    check_type(rounds, int, one_on_one_chat, 'rounds')
    check_min_val(rounds, 1, 'rounds')
    check_exact_val(len(personas), 2, 'len(personas)')


async def one_on_one_chat(question: str, personas: List[Persona], chatllm: ChatLLM, rounds: int = 5) -> None:
    _init_check(question, personas, chatllm, rounds)
    persona1 = deepcopy(chatllm)
    await persona1.set_system_prompt(personas[0])
    persona2 = deepcopy(chatllm)
    await persona2.set_system_prompt(personas[1])

    intro1 = await persona1('Who are you? Introduce yourself in short')
    intro2 = await persona2('Who are you? Introduce yourself in short')
    await persona1(intro2)
    await persona2(intro1)

    for i in range(rounds):
        reply = await persona2(question)
        question = await persona1(reply)
