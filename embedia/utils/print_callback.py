from embedia.schema.pubsub import Event
from embedia.utils.pubsub import subscribe_event
from embedia.utils.terminal_colors import colored
from typing import Optional


def print_callback(event_type: Event, id: int, timestamp: str, data: Optional[dict] = None):
    print(f"\n[time: {timestamp}] [id: {id}] [event: {event_type}]\n")
    if event_type == Event.LLMStart:
        msg = f"Prompt: {data['prompt']} ({data['prompt_tokens']} tokens)"
        color = 'cyan'
    elif event_type == Event.LLMEnd:
        msg = f"Completion: {data['completion']} ({data['completion_tokens']} tokens)"
        color = 'yellow'
    elif event_type == Event.ChatLLMInit:
        msg = f"{data['system_role']}: {data['system_content']} ({data['system_tokens']} tokens)"
        color = 'red'
    elif event_type == Event.ChatLLMStart:
        msg = f"{data['msg_role']}: {data['msg_content']} ({data['msg_tokens']} tokens)"
        color = 'cyan'
    elif event_type == Event.ChatLLMEnd:
        msg = f"{data['reply_role']}: {data['reply_content']} ({data['reply_tokens']} tokens)"
        color = 'yellow'
    elif event_type == Event.ToolStart:
        msg = f"Tool: {data['name']}\nArgs: {data['args']}\nKwargs: {data['kwargs']}"
        color = 'blue'
    elif event_type == Event.ToolEnd:
        msg = f"Tool: {data['name']}\nOutput: {data['output']}"
        color = 'blue'
    elif event_type == Event.EmbeddingStart:
        msg = f"Input: {data['input'][:100]}..."
        color = 'magenta'
    elif event_type == Event.EmbeddingEnd:
        msg = f"Embedding: {data['embedding'][:5]}..."
        color = 'magenta'
    elif event_type == Event.AgentStart:
        msg = f"Main Question: {data['question']}"
        color = 'cyan'
    elif event_type == Event.AgentStep:
        msg = (f"Question: {data['step'].question}\nToolChoice: {data['step'].action.tool_name}\n"
               f"ToolArgs: {data['step'].action.args}\nToolOutput: {data['step'].result.output}")
        color = 'yellow'
    elif event_type == Event.AgentEnd:
        msg = f"Final Answer: {data['answer']}"
        color = 'yellow'
    elif event_type == Event.AgentTimeout:
        msg = (f"Agent Timeout. Duration: {data['duration']}, No. of Steps: {data['num_steps']}\n",
               f"Step History: {data['step_history']}")
        color = 'red'
    else:
        raise ValueError(f"Unknown event type: {event_type}")
    print(colored(msg), color)


def setup_print_callback():
    subscribe_event(Event.LLMStart, print_callback)
    subscribe_event(Event.LLMEnd, print_callback)
    subscribe_event(Event.ChatLLMInit, print_callback)
    subscribe_event(Event.ChatLLMStart, print_callback)
    subscribe_event(Event.ChatLLMEnd, print_callback)
    subscribe_event(Event.ToolStart, print_callback)
    subscribe_event(Event.ToolEnd, print_callback)
    subscribe_event(Event.EmbeddingStart, print_callback)
    subscribe_event(Event.EmbeddingEnd, print_callback)
    subscribe_event(Event.AgentStart, print_callback)
    subscribe_event(Event.AgentStep, print_callback)
    subscribe_event(Event.AgentEnd, print_callback)
    subscribe_event(Event.AgentTimeout, print_callback)
