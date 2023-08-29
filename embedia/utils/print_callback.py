from embedia.utils.pubsub import subscribe_event
from embedia.utils.terminal_colors import colored
from embedia.schema.pubsub import Event


def print_llm_start_callback(data):
    print(colored(f"\nLLM: [id:{data['id']}] ({data['num_tokens']} tokens)\nPrompt: {data['prompt']}", 'blue'))


def print_llm_end_callback(data):
    print(colored(f"\nLLM: [id:{data['id']}] ({data['num_tokens']} tokens)\nCompletion: {data['completion']}", 'blue'))


def print_chatllm_init_callback(data):
    print(colored(f"\nChatLLM Init: [id:{data['id']}] ({data['num_tokens']} tokens)\n{data['role']}: {data['content']}", 'red'))


def print_chatllm_start_callback(data):
    print(colored(f"\nChatLLM Input: [id:{data['id']}] ({data['num_tokens']} tokens)\n{data['role']}: {data['content']}", 'red'))


def print_chatllm_end_callback(data):
    print(colored(f"\nChatLLM Output: [id:{data['id']}] ({data['num_tokens']} tokens)\n{data['role']}: {data['content']}", 'red'))


def print_tool_start_callback(data):
    print(colored(f"\nTool: [id:{data['id']}] {data['name']}\nArgs: {data['args']}\nKwargs: {data['kwargs']}",
                  'yellow'))


def print_tool_end_callback(data):
    output = data['output'][0]
    exit_code = data['output'][1]
    if exit_code == 0:
        print(colored(f"\nTool: [id:{data['id']}] {data['name']}\nOutput: {output}", 'yellow'))
    else:
        print(colored(f"\nTool: [id:{data['id']}] {data['name']}\nError: {output}", 'yellow'))


def print_embedding_start_callback(data):
    print(colored(f"\nEmbedding: [id:{data['id']}]\nInput excerpt: {data['input'][:100]}...", 'magenta'))


def print_embedding_end_callback(data):
    print(colored(f"\nEmbedding: [id:{data['id']}] ({len(data['embedding'])} dimensions)\nEmbedding excerpt: {data['embedding'][:5]}...", 'magenta'))


def print_agent_step_callback(data):
    print(f"\nAgent step:\n {data['action_step']}")


def print_agent_timeout_callback(data):
    print(f"\nAgent Timeout after duration: {data['duration']} and steps: {data['num_steps']}\n Action Steps:{data['action_steps']}")


def setup_print_callback():
    subscribe_event(Event.LLMStart, print_llm_start_callback)
    subscribe_event(Event.LLMEnd, print_llm_end_callback)
    subscribe_event(Event.ChatLLMInit, print_chatllm_init_callback)
    subscribe_event(Event.ChatLLMStart, print_chatllm_start_callback)
    subscribe_event(Event.ChatLLMEnd, print_chatllm_end_callback)
    subscribe_event(Event.ToolStart, print_tool_start_callback)
    subscribe_event(Event.ToolEnd, print_tool_end_callback)
    subscribe_event(Event.EmbeddingStart, print_embedding_start_callback)
    subscribe_event(Event.EmbeddingEnd, print_embedding_end_callback)
    subscribe_event(Event.AgentStep, print_agent_step_callback)
    subscribe_event(Event.AgentTimeout, print_agent_timeout_callback)
