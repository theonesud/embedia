from embedia.utils.pubsub import subscribe_event
from embedia.utils.terminal_colors import colored


def print_llm_start_callback(data):
    print(colored(f"\nLLM: [id:{data['id']}] ({data['num_tokens']} tokens)\nPrompt: {data['prompt']}", 'blue'))


def print_llm_end_callback(data):
    print(colored(f"\nLLM: [id:{data['id']}] ({data['num_tokens']} tokens)\nCompletion: {data['completion']}", 'blue'))


def print_chatllm_callback(data):
    print(colored(f"\nChatLLM: [id:{data['id']}] ({data['num_tokens']} tokens)\n{data['role']}: {data['content']}", 'red'))


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
    subscribe_event('llm_start', print_llm_start_callback)
    subscribe_event('llm_end', print_llm_end_callback)
    subscribe_event('chatllm_init', print_chatllm_callback)
    subscribe_event('chatllm_start', print_chatllm_callback)
    subscribe_event('chatllm_end', print_chatllm_callback)
    subscribe_event('tool_start', print_tool_start_callback)
    subscribe_event('tool_end', print_tool_end_callback)
    subscribe_event('embedding_start', print_embedding_start_callback)
    subscribe_event('embedding_end', print_embedding_end_callback)
    subscribe_event('agent_step', print_agent_step_callback)
    subscribe_event('agent_timeout', print_agent_timeout_callback)
