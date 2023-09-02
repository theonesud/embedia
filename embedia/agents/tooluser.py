import time
from copy import deepcopy
from typing import List, Tuple
import json

from embedia.core.chatllm import ChatLLM
from embedia.core.tool import Tool
from embedia.schema.agent import Action, Step
from embedia.schema.persona import Persona
from embedia.schema.pubsub import Event
from embedia.schema.tool import ToolReturn, ArgDocumentation, ToolDocumentation
from embedia.utils.exceptions import AgentError
from embedia.utils.pubsub import publish_event
from embedia.utils.typechecking import check_min_val, check_type


class ToolUser(Tool):
    def __init__(self, chatllm: ChatLLM, tools: List[Tool],
                 max_steps: int = 10, max_duration: int = 60) -> None:
        super().__init__(docs=ToolDocumentation(
            name="Tool User",
            desc="It uses the available tools to answer the user's question",
            args=[ArgDocumentation(
                name='question',
                desc='The main question that needs to be answered (Type: str)'
            )]))
        self.tools = tools
        self.max_steps = max_steps
        self.max_duration = max_duration
        check_type(chatllm, ChatLLM, self.__init__, 'chatllm')
        self.arg_chooser = deepcopy(chatllm)
        self.tool_chooser = deepcopy(chatllm)
        self.sys1_thinker = deepcopy(chatllm)
        self.step_history = []
        check_min_val(len(self.tools), 1, 'len(tools)')
        for tool in self.tools:
            check_type(tool, Tool, self.__init__, 'tool')

    async def _choose_tool(self, question: str) -> Tool:
        if len(self.tools) == 1:
            return self.tools[0]
        available_tools = "\n".join([f"{tool.docs.name}: {tool.docs.desc}" for tool in self.tools])
        prompt = (f"Question: {question}\n\n"
                  f"Tools:\n{available_tools}")
        await self.tool_chooser.set_system_prompt(Persona.ToolChooser)
        tool_choice = await self.tool_chooser(prompt)
        for tool in self.tools:
            if tool.docs.name == tool_choice:
                tool_choice = tool
                break
        if isinstance(tool_choice, str):
            raise AgentError(f"Agent's tool choice: {tool_choice} could not be found")
        return tool_choice

    async def _choose_args(self, question: str, tool_choice: Tool) -> dict:
        if len(tool_choice.docs.args) == 0:
            return {}
        arg_docs = ''
        for argdoc in tool_choice.docs.args:
            arg_docs += f"{argdoc.name}: {argdoc.desc}\n"
        prompt = (f"Question: {question}\n"
                  f"Function: {tool_choice.docs.desc}\n"
                  f"Arguments:\n{arg_docs}")

        await self.arg_chooser.set_system_prompt(Persona.ArgChooser)
        arg_choice = await self.arg_chooser(prompt)
        try:
            arg_choice = json.loads(arg_choice)
        except Exception:
            raise AgentError(f"Agent's arg choice: {arg_choice} could not be parsed")

        kwargs = {}
        available_args = [arg.name for arg in tool_choice.docs.args]
        for arg_name in arg_choice.keys():
            if arg_name not in available_args:
                raise AgentError(f"Argument choice: {arg_name} not found in Tool: {tool_choice.docs.name} Tool args: {available_args}")
            try:
                kwargs[arg_name] = eval(arg_choice[arg_name])
            except Exception:
                kwargs[arg_name] = arg_choice[arg_name]
        return kwargs

    async def _choose_next_step(self) -> Tuple[str, str]:
        await self.sys1_thinker.set_system_prompt(Persona.Sys1Thinker)

        prompt = f'Main question: {self.main_question}\n\n'
        for step in self.step_history:
            output_type = 'Output' if step.result.exit_code == 0 else 'Error'
            prompt += (f'Question: {step.question}\n'
                       f'{output_type}: {step.result.output}\n')

        resp = await self.sys1_thinker(prompt)
        if resp.split(':')[0] == 'Question':
            return resp.split(':')[1], 'Question'
        elif resp.split(':')[0] == 'Final Answer':
            return ':'.join(resp.split(':')[1:]), 'Final Answer'
        else:
            raise AgentError(f"Agent's response: {resp} could not be parsed")

    async def _run(self, question: str) -> ToolReturn:
        self.main_question = question
        publish_event(Event.AgentStart, id(self), {'question': question})
        steps = 1
        now = time.time()
        while steps <= self.max_steps and time.time() - now <= self.max_duration:

            if self.step_history:
                thought, thought_type = await self._choose_next_step()
                if thought_type == 'Question':
                    question = thought
                elif thought_type == 'Final Answer':
                    publish_event(Event.AgentEnd, id(self), {'question': self.main_question,
                                                             'answer': thought})
                    return ToolReturn(output=thought, exit_code=0)

            tool_choice = await self._choose_tool(question)
            kwargs = await self._choose_args(question, tool_choice)

            await self.human_confirmation({'tool': tool_choice.docs.name, 'args': kwargs})
            result = await tool_choice(**kwargs)

            step = Step(question=question,
                        action=Action(tool_name=tool_choice.docs.name,
                                      args=kwargs),
                        result=result)
            self.step_history.append(step)
            steps += 1
            publish_event(Event.AgentStep, id(self), {'question': step.question,
                                                      'tool': step.action.tool_name,
                                                      'tool_args': step.action.args,
                                                      'tool_output': step.result.output,
                                                      'tool_exit_code': step.result.exit_code})

        publish_event(Event.AgentTimeout, id(self), {'step_history': [x.serialize() for x in self.step_history],
                                                     'duration': f'{time.time() - now :.2f}s',
                                                     'num_steps': steps - 1})

        return ToolReturn(output=self.step_history[-1].result.output, exit_code=1)
