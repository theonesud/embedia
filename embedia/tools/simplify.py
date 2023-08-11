from embedia.tool import Tool
from typing import Type
from embedia.chatllm import ChatLLM
from embedia.message import Message


SIMPLIFY_SYSTEM = """Summarize content you are provided with for a second-grade student."""
# TODO: Write better arg docs


class Simplify(Tool):

    def __init__(self, chatllm: Type[ChatLLM]):
        super().__init__(name="Simplify",
                         desc="Simplify a text for a second-grade student",
                         args="text: str",
                         chatllm=chatllm)

    async def _run(self, text: str):
        simplify_expert = self.chatllm(system_prompt=SIMPLIFY_SYSTEM)
        command = await simplify_expert(Message(role='user', content=text))
        return command.content
