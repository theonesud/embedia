# ToolUser

This agent is designed to use recursively tools and answer the user's question.






An agent that uses the `available tools` to answer the `Main Question`.

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





class ToolUser(Tool):
    """


    """

    def __init__(self, chatllm: ChatLLM, tools: List[Tool],
                 max_steps: int = 10, max_duration: int = 60) -> None:
        """Constructor for the `ToolUser` class.

        Parameters
        ----------
        - `chatllm` (`ChatLLM`): The chatllm that is used to - choose the appropriate tool, choose the tool arguments, and choose the next step.
        - `tools` (List[`Tool`]): The tools available to the agent.
        - `max_steps` (int, optional): The maximum number of steps the agent can take. Defaults to 10.
        - `max_duration` (int, optional): The maximum duration of the agent in seconds. Defaults to 60.
        """

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

