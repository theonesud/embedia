import os
import pytest
from tests.utils import OpenAIChatLLM, OpenAITokenizer, OpenAILLM, Message, ChatLLM
os.makedirs('temp', exist_ok=True)

PANDAS_EXPERT_SYSTEM = """You are an expert in writing commands for the python pandas library.
Write one-line commands to solve the user's problems"""


# @pytest.mark.asyncio
# async def test_not_implemented_error_chatllm():
#     openai_chatllm = EmptyOpenAIChatLLM(PANDAS_EXPERT_SYSTEM, OpenAITokenizer(), 4096)
#     with pytest.raises(NotImplementedError):
#         await openai_chatllm(
#             Message(role='user',
#                     content=(
#                         'I want to extract all the '
#                         'pincodes in the column "address" and create '
#                         'another column "pincode"')))


@pytest.mark.asyncio
async def test_pandas_chatllm():
    openai_chatllm = OpenAIChatLLM()

    # await openai_chatllm(
    #     Message(role='user',
    #             content=('I want to extract all the '
    #                      'pincodes in the column "address" and create '
    #                      'another column "pincode"')))

    # await openai_chatllm(
    #     Message(role='user',
    #             content=('In the above command,'
    #                      'append "No" before each pincode')))

    # openai_chatllm.save_chat('temp/openai_chatllm.pkl')
    # openai_chatllm.load_chat('temp/openai_chatllm.pkl')

    # for message in openai_chatllm.chat_history:
    #     assert isinstance(message, Message)
    #     assert message.role in ('assistant', 'user', 'system')
    #     assert len(message.content) > 0


# @pytest.mark.asyncio
# async def test_pandas_without_msg_chatllm():
#     openai_chatllm = WithoutMessageOpenAIChatLLM(PANDAS_EXPERT_SYSTEM, OpenAITokenizer(), 4096)

#     with pytest.raises(ValueError):
#         await openai_chatllm(
#             Message(role='user',
#                     content=('I want to extract all the '
#                              'pincodes in the column "address" and create '
#                              'another column "pincode"')))


# @pytest.mark.asyncio
# async def test_pandas_extra_args_chatllm():
#     openai_chatllm = ExtraArgsOpenAIChatLLM(PANDAS_EXPERT_SYSTEM, OpenAITokenizer(), 4096)

#     with pytest.raises(ValueError):
#         await openai_chatllm(
#             Message(role='user',
#                     content=('I want to extract all the '
#                              'pincodes in the column "address" and create '
#                              'another column "pincode"')))


@pytest.mark.asyncio
async def test_llm_to_chatllm():
    openai_llm = OpenAILLM(OpenAITokenizer(), 4000)
    openai_chatllm = ChatLLM.from_llm(openai_llm, PANDAS_EXPERT_SYSTEM)

    await openai_chatllm(Message(
        role='user',
        content=('I want to extract all the pincodes '
                 'in the column "address" and create another column "pincode"')))

    await openai_chatllm(Message(role='user', content=('In the above command, append "No" '
                                                       'before each pincode')))

    openai_chatllm.save_chat('temp/openai_chatllm.pkl')
    openai_chatllm.load_chat('temp/openai_chatllm.pkl')

    for message in openai_chatllm.chat_history:
        assert isinstance(message, Message)
        assert message.role in ('assistant', 'user', 'system')
        assert len(message.content) > 0
