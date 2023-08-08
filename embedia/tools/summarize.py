from embedia.tool import Tool
from typing import Type
from embedia.chatllm import ChatLLM
from embedia.message import Message


SUMMARIZE_SYSTEM = """You will be provided with some content, and your task is to summarize it
in the following format:

-Overall summary of the content
-Important details from the content
-Any conclusions derived from the content"""


class Summarize(Tool):

    def __init__(self, chatllm: Type[ChatLLM]):
        super().__init__(name="Summarize",
                         desc="Summarize a text with overall summary, important details, \
                            and conclusions",
                         examples="Hello World!",
                         args="text: str",
                         returns="summary: str",
                         chatllm=chatllm)

    async def _run(self, text: str):
        summarize_expert = self.chatllm(system_prompt=SUMMARIZE_SYSTEM)
        command = await summarize_expert.reply(Message(role='user', content=text))
        return command.content
