from embedia.utils.pubsub import subscribe_event
from embedia.utils.terminal_colors import colored


def print_chatllm_init_callback(data):
    print(colored(f"\nSystem:\n{data['system_prompt']}", 'red'))


def print_chatllm_save_callback(data):
    print(colored(f"\nChatLLM saved to filepath: {data['filepath']}", 'cyan'))


def print_chatllm_loaded_callback(data):
    print(colored(f"\nChatLLM loaded from filepath: {data['filepath']}", 'cyan'))


def print_chatllm_start_callback(data):
    print(colored(f"\n{data['message_role']}:\n{data['message_content']}",
                  'green'))


def print_chatllm_end_callback(data):
    print(colored(f"\n{data['reply_role']}:\n{data['reply_content']}",
                  'green'))


def print_tool_start_callback(data):
    print(colored(f"\nTool: {data['name']} started with args: {data['args']} and kwargs: {data['kwargs']}",
                  'yellow'))


def print_tool_end_callback(data):
    output = data['output'][0]
    exit_code = data['output'][1]
    if exit_code == 0:
        print(colored(f"\nTool: {data['name']} finished with output:\n{output}", 'yellow'))
    else:
        print(colored(f"\nTool: {data['name']} finished with error:\n{output}", 'yellow'))


def print_llm_start_callback(data):
    print(colored(f"\nLLM started with args: {data['args']} and kwargs: {data['kwargs']}", 'blue'))


def print_llm_end_callback(data):
    print(colored(f"\nLLM finished with completion: {data['completion']}", 'blue'))


def print_embedding_start_callback(data):
    print(colored(f"\nCreating embedding. num_tokens: {data['num_tokens']} text excerpt: {data['input'][:100]}...", 'magenta'))


def print_embedding_end_callback(data):
    print(colored(f"\nEmbedding created. len: {len(data['embedding'])} embedding excerpt: {data['embedding'][:5]}...", 'magenta'))


def print_agent_step_callback(data):
    print(f"\nAgent step:\n {data['action_step']}")


def print_agent_timeout_callback(data):
    print(f"\nAgent Timeout after duration: {data['duration']} and steps: {data['num_steps']}\n Action Steps:{data['action_steps']}")


def setup_print_callback():
    subscribe_event('chatllm_init', print_chatllm_init_callback)
    subscribe_event('chatllm_saved', print_chatllm_save_callback)
    subscribe_event('chatllm_loaded', print_chatllm_loaded_callback)
    subscribe_event('chatllm_start', print_chatllm_start_callback)
    subscribe_event('chatllm_end', print_chatllm_end_callback)
    subscribe_event('tool_start', print_tool_start_callback)
    subscribe_event('tool_end', print_tool_end_callback)
    subscribe_event('llm_start', print_llm_start_callback)
    subscribe_event('llm_end', print_llm_end_callback)
    subscribe_event('embedding_start', print_embedding_start_callback)
    subscribe_event('embedding_end', print_embedding_end_callback)
    subscribe_event('agent_step', print_agent_step_callback)
    subscribe_event('agent_timeout', print_agent_timeout_callback)
