from embedia import Tool
from typing import Type
from embedia import ChatLLM, Message


SIMPLIFY_SYSTEM = """Summarize content you are provided with for a second-grade student."""


class Simplify(Tool):

    def __init__(self, chatllm: Type[ChatLLM]):
        super().__init__(name="Simplify",
                         desc="Simplify a text for a second-grade student",
                         args={"text": "The text to be simplified"},
                         chatllm=chatllm)

    async def _run(self, text: str):
        simplify_expert = self.chatllm(system_prompt=SIMPLIFY_SYSTEM)
        command = await simplify_expert(Message(role='user', content=text))
        return command.content, 0
