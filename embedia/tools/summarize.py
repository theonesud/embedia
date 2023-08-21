from typing import Type

from embedia.core.chatllm import ChatLLM
from embedia.core.tool import Tool
from embedia.schema.message import Message

# SUMMARIZE_SYSTEM = """You will be provided with some content, and your task is to summarize it
# in the following format:

# -Overall summary of the content
# -Important details from the content
# -Any conclusions derived from the content"""


# class Summarize(Tool):

#     def __init__(self, chatllm: Type[ChatLLM]):
#         super().__init__(name="Summarize",
#                          desc=("Summarize a text with overall summary, important details, "
#                                "and conclusions"),
#                          args={"text": "The text to be summarized"},
#                          chatllm=chatllm)

#     async def _run(self, text: str):
#         summarize_expert = self.chatllm(system_prompt=SUMMARIZE_SYSTEM)
#         command = await summarize_expert(Message(role='user', content=text))
#         return command.content, 0
