from embedia.tool import Tool
from typing import Type, List, Optional
from embedia.chatllm import ChatLLM
from embedia.message import Message
from embedia.scratchpad import ScratchpadEntry
import time
import inspect

# AGENT_SYSTEM = """You're an agent designed to solve the user's problems using the tools they provide you.
# You only use the tools that are explicitly provided to you. If a tool is not explicitly provided, you cannot use it.
# Tools has args that you need to provide in order to use them. Each tool's documentation is provided in the following format:

# Name: <name of the tool>
# Description: <description of the tool>
# Examples: <examples of how to use it>
# Args: <arguments that the tool takes>
# Returns: <what the tool returns>

# The most important part of the documentation is the Args section. It tells you what arguments the tool takes and what they mean. Very carefully read the Args section of the documentation before using a tool.
# Only use the tools that are explicitly provided to you.

# Use the following format for your response:
# Thought: <Reasoning behind the choice of tool and the choice of arguments>
# Tool: <Tool name>
# Args: <Tool arguments>
# """

TOOL_CHOOSER = """You're an expert in choosing the best tool for answering the user's question.
The list of tools and their descriptions will be provided to you.
Reply with the name of the chosen tool and nothing else.
"""

ARG_CHOOSER = """You're an expert in choosing the values of function arguments based on the user's question.
The list of arguments and their descriptions will be provided to you.
Reply with values of all arguments in the following format:
<argument name>: <argument value>
<argument name>: <argument value>
<argument name>: <argument value>
Do not reply with anything else.
"""


class Agent(Tool):
    def __init__(self, chatllm: Type[ChatLLM], tools: Optional[List[Tool]] = None,
                 max_steps: int = 10, max_time: int = 60):
        super().__init__(name="Agent",
                         desc="Use the available tools to solve problems",
                         examples="How many lines of code does this folder have?",
                         args="question: str",
                         returns="output: str",
                         chatllm=chatllm)
        self.scratchpad: List[ScratchpadEntry] = []
        self.tools = tools
        # self.max_steps = max_steps
        # self.max_time = max_time
        self.chatllm = chatllm

    async def _run(self, question: str):

        if len(self.tools) == 0:
            raise ValueError('No tools provided to Agent, Acting as a ChatLLM')
        elif len(self.tools) == 1:
            tool_choice = self.tools[0]
        else:
            available_tools = "\n".join([f"{tool.name}: {tool.desc}" for tool in self.tools])
            prompt = (f"Question: {question}\n\n"
                      f"Tools:\n{available_tools}")
            tool_chooser = self.chatllm(system_prompt=TOOL_CHOOSER)
            tool_choice = await tool_chooser(Message(role='user', content=prompt))
            tool_choice = tool_choice.content
            for tool in self.tools:
                if tool.name == tool_choice:
                    tool_choice = tool
                    break
            if isinstance(tool_choice, str):
                raise ValueError(f"Agent's tool choice: {tool_choice} could not be found")

        prompt = (f"Question: {question}\n\n"
                  f"Arguments:\n{tool_choice.args}")

        arg_chooser = self.chatllm(system_prompt=ARG_CHOOSER)
        arg_choice = await arg_chooser(Message(role='user', content=prompt))
        arg_choice = arg_choice.content
        arg_choice = arg_choice.split('\n')
        arg_choice_dict = {}
        for choice in arg_choice:
            choice = choice.split(':')
            if len(choice) != 2:
                raise ValueError(f"Agent's arg choice: {choice} could not be parsed")
            arg_name = choice[0].strip()
            arg_value = choice[1].strip()
            arg_choice_dict[arg_name] = arg_value

        argspec = inspect.getfullargspec(tool_choice._run)
        arg_names = argspec.args
        annotations = argspec.annotations
        kwargs = {}
        for arg_name in arg_names:
            if arg_name == 'self':
                continue
            assert arg_name in arg_choice_dict.keys(
            ), f"Argument: {arg_name} not found in Agent's args choice: {arg_choice_dict}"
            if annotations.get(arg_name) != str:
                kwargs[arg_name] = eval(arg_choice_dict[arg_name])
            else:
                kwargs[arg_name] = arg_choice_dict[arg_name]

        tool_choice.confirm_before_running(**kwargs)
        observation = await tool_choice(**kwargs)
        print(observation)
        # print(arg_choice)

        # steps = 1
        # now = time.time()
        # self.scratchpad.append(ScratchpadEntry(question=command))
        # while steps <= self.max_steps and time.time() - now <= self.max_time:

        # if self.scratchpad[-1].question:
        #     content = self.scratchpad[-1].question
        # elif self.scratchpad[-1].observation:
        #     content = self.scratchpad[-1].observation
        # tools_docstrings = '\n'.join([tool.docstring for tool in self.tools])
        # command = AGENT_MESSAGE.format(tools_docstrings=tools_docstrings, problem=command)

        # response = await self.agent(Message(role='user', content=command))
        # response = response.content
        # print('------------>', response)
        # response = response.split('\n')
        # assert response[0][:7] == 'Thought'
        # if len(response) == 3:
        #     assert response[1][:4] == 'Tool'
        #     assert response[2][:4] == 'Args'
        #     try:
        #         # self.confirm_before_running(tool=response[1], args=response[2])
        #         # get tool from self.tools
        #         # run tool with args
        #         # observation = response
        #         observation = input()
        #     except Exception as e:
        #         # observation = error
        #         observation = str(e)
        #     self.scratchpad.append(ScratchpadEntry(thought=response[0],
        #                                            tool=response[1],
        #                                            args=response[2],
        #                                            observation=observation))
        # elif len(response) == 2:
        #     assert response[1][:6] == 'Answer'
        #     self.scratchpad.append(ScratchpadEntry(thought=response[0],
        #                                            answer=response[1]))
        #     break
        # steps += 1
        # return self.scratchpad[-1].answer

        # async def backup_run(self, command: str):
        #     steps = 1
        #     now = time.time()
        #     self.scratchpad.append(ScratchpadEntry(question=command))
        #     while steps <= self.max_steps and time.time() - now <= self.max_time:

        #         if self.scratchpad[-1].question:
        #             content = self.scratchpad[-1].question
        #         elif self.scratchpad[-1].observation:
        #             content = self.scratchpad[-1].observation
        #         response = await self.agent(Message(role='user', content=content))
        #         response = response.content
        #         response = response.split('\n')
        #         assert response[0][:7] == 'Thought'
        #         if len(response) == 3:
        #             assert response[1][:4] == 'Tool'
        #             assert response[2][:4] == 'Args'
        #             try:
        #                 self.confirm_before_running(tool=response[1], args=response[2])
        #                 # get tool from self.tools
        #                 # run tool with args
        #                 # observation = response
        #                 observation = None
        #             except Exception:
        #                 # observation = error
        #                 observation = None
        #             self.scratchpad.append(ScratchpadEntry(thought=response[0],
        #                                                    tool=response[1],
        #                                                    args=response[2],
        #                                                    observation=observation))
        #         elif len(response) == 2:
        #             assert response[1][:6] == 'Answer'
        #             self.scratchpad.append(ScratchpadEntry(thought=response[0],
        #                                                    answer=response[1]))
        #             break
        #         steps += 1
        #     return self.scratchpad[-1].answer
