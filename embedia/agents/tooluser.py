import json
import time
from copy import deepcopy
from typing import List, Tuple

from embedia.core.chatllm import ChatLLM
from embedia.core.tool import Tool
from embedia.schema.agent import Action, Step
from embedia.schema.persona import Persona
from embedia.schema.pubsub import Event
from embedia.schema.tool import ParamDocumentation, ToolDocumentation, ToolReturn
from embedia.utils.exceptions import AgentError
from embedia.utils.pubsub import publish_event
from embedia.utils.typechecking import check_min_val, check_type


class ToolUserAgent(Tool):
    """An agent that uses the `available tools` to answer the `Main Question`.

    It runs the following loop internally:
    - Choose a tool based on the question. (For the first step, the question is the `Main Question`)
    - Choose the arguments for the chosen tool.
    - Ask for human confirmation before running the chosen tool with the chosen arguments.
    - Run the tool with the chosen arguments and save the output as the `Step Result`.
    - Decide whether to ask itself another question (continue the loop) or to return the `Step Result` as the `Final Answer`.

    In summary, this agent can decide which tool to run, run them with the proper arguments, observe their outputs, and decide what to do next.
    If it decides to ask itself another question, it'll choose the appropriate tool and its arguments and repeat the above process.

    The loop runs for a maximum of `max_steps` steps or `max_duration` seconds (whichever happens first).
    Since this agent is a subclass of `Tool`, it can be used as a tool in another agent.

    Attributes
    ----------
    - `tools` (List[`Tool`]): The tools available to the agent.
    - `max_steps` (int): The maximum number of steps the agent can take.
    - `max_duration` (int): The maximum duration the agent can run in seconds.
    - `main_question` (str): The main question to answer.
    - `step_history` (List[`Step`]): The history of steps taken by the agent.
    """

    def __init__(
        self,
        chatllm: ChatLLM,
        tools: List[Tool],
        max_steps: int = 10,
        max_duration: int = 60,
    ) -> None:
        """Constructor for the `ToolUserAgent` class.

        Parameters
        ----------
        - `chatllm` (`ChatLLM`): The chatllm that is used to - choose the appropriate tool, choose the tool arguments, and choose the next step.
        - `tools` (List[`Tool`]): The tools available to the agent.
        - `max_steps` (int, optional): The maximum number of steps the agent can take. Defaults to 10.
        - `max_duration` (int, optional): The maximum duration (in seconds) the agent is allowed to run. Defaults to 60.
        """
        super().__init__(
            docs=ToolDocumentation(
                name="Tool User",
                desc="It uses the available tools to answer the user's question",
                params=[
                    ParamDocumentation(
                        name="question",
                        desc="The main question that needs to be answered (Type: str)",
                    )
                ],
            )
        )
        self.tools = tools
        self.max_steps = max_steps
        self.max_duration = max_duration
        check_type(chatllm, ChatLLM, self.__init__, "chatllm")
        self.arg_chooser = deepcopy(chatllm)
        self.tool_chooser = deepcopy(chatllm)
        self.sys1_thinker = deepcopy(chatllm)
        self.step_history: List[Step] = []
        check_min_val(len(self.tools), 1, "len(tools)")
        for tool in self.tools:
            check_type(tool, Tool, self.__init__, "tool")

    async def _choose_tool(self, question: str) -> Tool:
        """Choose a tool based on the question.
        If there is only one tool available, it is automatically chosen.
        Otherwise, a `ToolChooser` persona is used to choose the tool.

        Parameters
        ----------
        - `question` (str): The question to answer.

        Returns
        -------
        - `tool_choice` (`Tool`): The tool chosen by the agent.

        Raises
        ------
        - `AgentError`: If the chosen tool was not found in the list of available tools.
        """
        if len(self.tools) == 1:
            return self.tools[0]
        available_tools = "\n".join(
            [f"{tool.docs.name}: {tool.docs.desc}" for tool in self.tools]
        )
        prompt = f"Question: {question}\n\n Tools:\n{available_tools}"
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
        """Choose the arguments for the chosen tool.
        If the tool has no parameters, an empty dictionary is returned.
        Otherwise, an `ArgChooser` persona is used to choose the arguments.

        Parameters
        ----------
        - `question` (str): The question to answer.
        - `tool_choice` (`Tool`): The tool chosen by the agent.

        Returns
        -------
        - `kwargs` (dict): The arguments chosen by the agent.

        Raises
        ------
        - `AgentError`: If the chosen param was not found in the tool's params or if the argument could not be parsed.
        """
        if len(tool_choice.docs.params) == 0:
            return {}
        param_docs = ""
        for paramdoc in tool_choice.docs.params:
            param_docs += f"{paramdoc.name}: {paramdoc.desc}\n"
        prompt = (
            f"Question: {question}\n"
            f"Function: {tool_choice.docs.desc}\n"
            f"Parameters:\n{param_docs}"
        )

        await self.arg_chooser.set_system_prompt(Persona.ArgChooser)
        arg_choice = await self.arg_chooser(prompt)
        try:
            arg_choice = json.loads(arg_choice)
        except Exception as e:
            raise AgentError(
                f"Agent's arg choice: {arg_choice} could not be parsed"
            ) from e

        kwargs = {}
        available_params = [param.name for param in tool_choice.docs.params]
        for param in arg_choice.keys():
            if param not in available_params:
                raise AgentError(
                    f"Parameter: {param} not found in Tool: {tool_choice.docs.name} Tool params: {available_params}"
                )
            try:
                kwargs[param] = eval(arg_choice[param])
            except Exception:
                kwargs[param] = arg_choice[param]
        return kwargs

    async def _choose_next_step(self) -> Tuple[str, str]:
        """Choose the next step.
        The `Sys1Thinker` persona is used to choose the next step.
        It takes into consideration the main question and all the steps taken so far, and chooses the next step.
        The next step can either be to ask itself another question or to return the final answer.

        Returns
        -------
        - Tuple(`thought`:str, `thought_type`:str): The next step chosen by the agent.
            If `thought_type` is `Question`, then `thought` is the question to ask itself.
            If `thought_type` is `Final Answer`, then `thought` is the final answer to return to the user.

        Raises
        ------
        - `AgentError`: If the agent's response could not be parsed.
        """
        await self.sys1_thinker.set_system_prompt(Persona.Sys1Thinker)

        prompt = f"Main question: {self.main_question}\n\n"
        for step in self.step_history:
            output_type = "Output" if step.result.exit_code == 0 else "Error"
            prompt += (
                f"Question: {step.question}\n {output_type}: {step.result.output}\n"
            )

        resp = await self.sys1_thinker(prompt)
        if resp.split(":")[0] == "Question":
            return resp.split(":")[1], "Question"
        elif resp.split(":")[0] == "Final Answer":
            return ":".join(resp.split(":")[1:]), "Final Answer"
        else:
            raise AgentError(f"Agent's response: {resp} could not be parsed")

    async def _run(self, question: str) -> ToolReturn:
        """Run the agent for a maximum of `max_steps` steps or `max_duration` seconds (whichever happens first)

        It runs the following loop internally:
        - Choose a tool based on the question. (For the first step, the question is the `Main Question`)
        - Choose the arguments for the chosen tool.
        - Ask for human confirmation before running the chosen tool with the chosen arguments.
        - Run the tool with the chosen arguments and save the output as the `Step Result`.
        - Decide whether to ask itself another question (continue the loop) or to return the `Step Result` as the `Final Answer`.

        Parameters
        ----------
        - `question` (str): The main question to answer.

        Returns
        -------
        - `output` (`ToolReturn`): The final answer to return to the user or the output of the last step.
            If the agent times out, the output of the last step is returned.
            If the agent found the final answer before timing out, the final answer is returned.
        """
        self.main_question = question
        publish_event(Event.AgentStart, id(self), {"question": question})
        steps = 1
        now = time.time()
        while steps <= self.max_steps and time.time() - now <= self.max_duration:
            if self.step_history:
                thought, thought_type = await self._choose_next_step()
                if thought_type == "Question":
                    question = thought
                elif thought_type == "Final Answer":
                    publish_event(
                        Event.AgentEnd,
                        id(self),
                        {"question": self.main_question, "answer": thought},
                    )
                    return ToolReturn(output=thought, exit_code=0)

            tool_choice = await self._choose_tool(question)
            kwargs = await self._choose_args(question, tool_choice)

            await self.human_confirmation(
                {"tool": tool_choice.docs.name, "args": kwargs}
            )
            result = await tool_choice(**kwargs)

            step = Step(
                question=question,
                action=Action(tool_name=tool_choice.docs.name, args=kwargs),
                result=result,
            )
            self.step_history.append(step)
            steps += 1
            publish_event(
                Event.AgentStep,
                id(self),
                {
                    "question": step.question,
                    "tool": step.action.tool_name,
                    "tool_args": step.action.args,
                    "tool_output": step.result.output,
                    "tool_exit_code": step.result.exit_code,
                },
            )

        publish_event(
            Event.AgentTimeout,
            id(self),
            {
                "step_history": [x.serialize() for x in self.step_history],
                "duration": f"{time.time() - now :.2f}s",
                "num_steps": steps - 1,
            },
        )

        return ToolReturn(output=self.step_history[-1].result.output, exit_code=1)
