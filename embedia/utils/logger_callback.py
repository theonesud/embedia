from embedia.utils.pubsub import subscribe_event
from embedia.utils.terminal_colors import colored


def logger_chatllm_init_callback(data):
    print(colored(f"\nSystem:\n{data['system_prompt']}", 'red'))


def logger_chatllm_save_callback(data):
    print(colored(f"\nChatLLM saved to filepath: {data['filepath']}", 'cyan'))


def logger_chatllm_loaded_callback(data):
    print(colored(f"\nChatLLM loaded from filepath: {data['filepath']}", 'cyan'))


def logger_chatllm_start_callback(data):
    print(colored(f"\n{data['message_role']}:\n{data['message_content']}",
                  'green'))


def logger_chatllm_end_callback(data):
    print(colored(f"\n{data['reply_role']}:\n{data['reply_content']}",
                  'green'))


def logger_tool_start_callback(data):
    print(colored(f"\nTool: {data['name']} started with args: {data['args']} and kwargs: {data['kwargs']}",
                  'yellow'))


def logger_tool_end_callback(data):
    output = data['output'][0]
    exit_code = data['output'][1]
    if exit_code == 0:
        print(colored(f"\nTool: {data['name']} finished with output:\n{output}", 'yellow'))
    else:
        print(colored(f"\nTool: {data['name']} finished with error:\n{output}", 'yellow'))


def logger_llm_start_callback(data):
    print(colored(f"\nLLM started with args: {data['args']} and kwargs: {data['kwargs']}", 'blue'))


def logger_llm_end_callback(data):
    print(colored(f"\nLLM finished with completion: {data['completion']}", 'blue'))


def setup_logger_callback():
    subscribe_event('chatllm_init', logger_chatllm_init_callback)
    subscribe_event('chatllm_saved', logger_chatllm_save_callback)
    subscribe_event('chatllm_loaded', logger_chatllm_loaded_callback)
    subscribe_event('chatllm_start', logger_chatllm_start_callback)
    subscribe_event('chatllm_end', logger_chatllm_end_callback)
    subscribe_event('tool_start', logger_tool_start_callback)
    subscribe_event('tool_end', logger_tool_end_callback)
    subscribe_event('llm_start', logger_llm_start_callback)
    subscribe_event('llm_end', logger_llm_end_callback)
