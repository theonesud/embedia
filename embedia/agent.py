from embedia.tool import Tool
from typing import Type, List, Optional, Tuple, Any
from embedia.chatllm import ChatLLM
from embedia.message import Message
from embedia.scratchpad import ScratchpadEntry
import time
import inspect

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

SYSTEM_1_THINKER = """You're an expert in deciding whether we've reached the final answer or not.
If we've reached the final answer, reply with the answer in the following format:
Final Answer: <final answer>
If not, reply with the first plan of action that comes to you in the following format:
Thought: <next step>
Do not reply with anything else.
"""


class Agent(Tool):
    def __init__(self, chatllm: Type[ChatLLM], tools: Optional[List[Tool]] = None,
                 max_steps: int = 2, max_time: int = 60) -> None:
        super().__init__(name="Agent",
                         desc="Use the available tools to solve problems",
                         args={'question': 'The input question from the user'},
                         chatllm=chatllm)
        self.scratchpad: List[ScratchpadEntry] = []
        self.tools = tools
        self.max_steps = max_steps
        self.max_time = max_time
        self.chatllm = chatllm
        if len(self.tools) == 0:
            raise ValueError('No tools provided to Agent, Should Act as a ChatLLM?')

    async def _choose_tool(self, question: str) -> Tool:
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
        return tool_choice

    async def _choose_args(self, question: str, tool_choice: Tool) -> dict:
        arg_docs = ''
        for arg_key, arg_desc in tool_choice.args.items():
            arg_docs += f"{arg_key}: {arg_desc}\n"
        prompt = (f"Question: {question}\n\n"
                  f"Arguments:\n{arg_docs}")

        arg_chooser = self.chatllm(system_prompt=ARG_CHOOSER)
        arg_choice = await arg_chooser(Message(role='user', content=prompt))
        arg_choice = arg_choice.content
        arg_choice = arg_choice.split('\n')
        arg_choice_dict = {}
        for choice in arg_choice:
            choice = choice.split(':')
            # if len(choice) != 2:
            #     raise ValueError(f"Agent's arg choice: {choice} could not be parsed")
            arg_name = choice[0].strip()
            arg_value = ':'.join(choice[1:]).strip()
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
        return kwargs

    async def _run(self, question: str) -> Tuple[Any, int]:
        steps = 1
        now = time.time()
        while steps <= self.max_steps and time.time() - now <= self.max_time:

            self.sys1 = self.chatllm(system_prompt=SYSTEM_1_THINKER)
            if self.scratchpad:
                prompt = "\n".join([str(entry) for entry in self.scratchpad])
            else:
                prompt = question
            resp = await self.sys1(Message(role='user', content=prompt))
            resp = resp.content
            if resp.split(':')[0] == 'Thought':
                question = resp.split(':')[1]
            elif resp.split(':')[0] == 'Final Answer':
                return resp.split(':')[1]
            else:
                raise ValueError(f"Agent's response: {resp} could not be parsed")

            if len(self.tools) == 1:
                tool_choice = self.tools[0]
            else:
                tool_choice = await self._choose_tool(question)
            kwargs = await self._choose_args(question, tool_choice)
            tool_choice.confirm_before_running(**kwargs)
            observation = await tool_choice(**kwargs)
            self.scratchpad.append(ScratchpadEntry(question=question,
                                                   tool=tool_choice.name,
                                                   args=kwargs,
                                                   observation=observation))
            steps += 1

        return self.scratchpad[-1].observation, 0
