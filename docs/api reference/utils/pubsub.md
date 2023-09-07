# Publish-Subscribe Event System

Every major class in `Embedia` publishes events at important moments in its execution. These events are subscribed by two pre-defiend set of subscribers:
- One that prints (color coded) all the 4 datapoints in `stdout`
- One that backs-up all the 4 datapoints to a sqlite3 db stored in `~/.embedia/backup.db`

You can also create your own subscribers to do whatever you want with the data (more on that below).

## Types of Events
The current list of possible events are the following:

- `LLMStart`: Before the `LLM` class sends the prompt to the LLM
- `LLMEnd`: After the `LLM` class recieves the response from the LLM
- `ChatLLMInit`: After the `system_prompt` of a `ChatLLM` class is set
- `ChatLLMStart`: Before the `ChatLLM` class sends the message to the LLM
- `ChatLLMEnd`: After the `ChatLLM` class recieves the message from the LLM
- `ToolStart`: Before running the `_run` function in `Tool`
- `ToolEnd`: After getting the response from the `_run` function from `Tool`
- `EmbeddingStart`: Before an embedding is created by the `EmbeddingModel` class
- `EmbeddingEnd`: After the `EmbeddingModel` creates an embedding
- `AgentStart`: Before starting the agent loop
- `AgentStep`: After each cycle in the agent loop is complete
- `AgentEnd`: If the agent found the final answer and is returning it to the user
- `AgentTimeout`: If the agent timed-out either by exceding the `max_steps` or `max_duration` it can run.

You can find the list of possible events by printing the `Event` enum like so:

```python
>>> from embedia import Event
>>> Event._member_names_
>>> ['LLMStart', 'LLMEnd', 'ChatLLMInit', 'ChatLLMStart', 'ChatLLMEnd', 'ToolStart', 'ToolEnd', 'EmbeddingStart', 'EmbeddingEnd', 'AgentStart', 'AgentStep', 'AgentEnd', 'AgentTimeout']
```

## Publishing an Event

While publishing an event, the below datapoints are sent to the Publish-Subscribe System. Every subscriber of that event will recieve all the 4 datapoints when that happens:
- `event_type`: One of the `Event` enum values
- `id`: The instance id of the variable firing the event
- `timestamp`: The current time with the timezone
- `data`: A dictionary containing information related to the event

The `data` field published for each event is as follows:

- `LLMStart`
```json
{
    "prompt": "The prompt that is being sent to the LLM",
    "prompt_tokens": "Number of tokens in the prompt"
}
```
- `LLMEnd`
```json
{
    "prompt": "The prompt that is being sent to the LLM",
    "prompt_tokens": "Number of tokens in the prompt",
    "completion": "The completion recieved from the LLM",
    "completion_tokens": "Number of tokens in the completion"
}
```
- `ChatLLMInit`
```json
{
    "system_role": "Literal string - 'system'",
    "system_content": "The system prompt",
    "system_tokens": "Number of tokens in the system prompt"
}
```
- `ChatLLMStart`
```json
{
    "msg_role": "Literal string - 'user'",
    "msg_content": "The message contents being sent to the LLM",
    "msg_tokens": "Number of tokens in the message contents"
}
```
- `ChatLLMEnd`
```json
{
    "msg_role": "Literal string - 'user'",
    "msg_content": "The message contents being sent to the LLM",
    "msg_tokens": "Number of tokens in the message contents",
    "reply_role": "Literal string - 'assistant'",
    "reply_content": "The reply message contents recieved from the LLM",
    "reply_tokens": "Number of tokens in the reply message contents"
}
```
- `ToolStart`
```json
{
    "name": "The name of the tool (subclass of `Tool`) being run",
    "args": "The arguments passed to the tool",
    "kwargs": "The keyword arguments passed to the tool"
}
```
- `ToolEnd`
```json
{
    "name": "The name of the tool (subclass of `Tool`) being run",
    "args": "The arguments passed to the tool",
    "kwargs": "The keyword arguments passed to the tool",
    "tool_output": "The output of the tool",
    "tool_exit_code": "The exit code of the tool (0 if successful, 1 if failed)"
}
```
- `EmbeddingStart`
```json
{
    "input": "The input text to the embedding model"
}
```
- `EmbeddingEnd`
```json
{
    "input": "The input text to the embedding model",
    "embedding": "The embedding created by the embedding model"
}
```
- `AgentStart`
```json
{
    "question": "The main question asked by the user",
}
```
- `AgentStep`
```json
{
    "question": "Question the agent is trying to answer in this step",
    "tool": "The tool name chosen by the agent for answering this question",
    "tool_args": "The arguments chosen to be passed to the tool",
    "tool_output": "The output of the tool",
    "tool_exit_code": "The exit code of the tool (0 if successful, 1 if failed)",
}
```
- `AgentEnd`
```json
{
    "question": "The main question asked by the user",
    "answer": "The final answer found by the agent"
}
```
- `AgentTimeout`
```json
{
    "step_history": "A list of every step taken by the agent",
    "duration": "The number of seconds the agent ran for",
    "num_steps": "The number of steps the agent took"
}
```

# Subscribing to an Event

You can create your own event subscribers in case you want to execute some code whenever a certain event occurs.

To do so, you can use the `subscribe_event` function. In the following example, we create a custom subscriber for the `ChatLLMEnd` event. A reason why you would want to do that is to keep a track of the number of tokens that have been consumed (if you are using a third party service like OpenAI) to keep a track of costs.

```python
from embedia import Event, subscribe_event

total_tokens = 0

def track_cost(event_type: Event, id: int, timestamp: str, data: Optional[dict] = None) -> None:
    total_tokens += data["msg_tokens"] + data["reply_tokens"]
    total_cost = total_tokens * 0.000002
    print(f"Approximate bill so far: {total_cost} USD")

subscribe_event(Event.ChatLLMEnd, track_cost)
```
> Note that this is just an example. Please consider the actual costs of the service you are using and modify the code accordingly.

> Also note that the `data["msg_tokens"]` and `data["reply_tokens"]` will be `None` if the `ChatLLM` subclass doesnt provide a `Tokenizer` class in the constructor. Please refer the `ChatLLM` documentation for more details.

> Also note that currently the pubsub system is synchronous. We might make it asynchronous in the future.

If the above example code runs before you use any subclass of `ChatLLM`, then the `track_cost` function will be called every time the `ChatLLMEnd` event is published. As described in the code, it'll print the approximate bill so far.