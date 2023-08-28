from embedia.utils.pubsub import subscribe_event
import logging
import json
import os
home = os.path.expanduser('~')
os.makedirs(f'{home}/.embedia', exist_ok=True)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f'{home}/.embedia/backup.log')
formatter = logging.Formatter(
    fmt="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def file_llm_callback(data):
    logger.info('LLM>' + json.dumps(data, indent=2))


def file_chatllm_callback(data):
    logger.info('ChatLLM>' + json.dumps(data, indent=2))


def file_tool_callback(data):
    logger.info('Tool>' + json.dumps(data, indent=2))


def file_agent_callback(data):
    logger.info('Agent>' + json.dumps(data, indent=2))


def setup_file_callback():
    subscribe_event('llm_start', file_llm_callback)
    subscribe_event('llm_end', file_llm_callback)
    subscribe_event('chatllm_init', file_chatllm_callback)
    subscribe_event('chatllm_start', file_chatllm_callback)
    subscribe_event('chatllm_end', file_chatllm_callback)
    subscribe_event('tool_start', file_tool_callback)
    subscribe_event('tool_end', file_tool_callback)
    subscribe_event('agent_step', file_agent_callback)
    subscribe_event('agent_timeout', file_agent_callback)


# TODO: make them enum
# TODO: make async
# TODO: make print using logging
# TODO: make time with timezone
