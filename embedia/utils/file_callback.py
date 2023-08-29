from embedia.utils.pubsub import subscribe_event
import logging
import json
import os
from embedia.schema.pubsub import Event

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
    subscribe_event(Event.LLMStart, file_llm_callback)
    subscribe_event(Event.LLMEnd, file_llm_callback)
    subscribe_event(Event.ChatLLMInit, file_chatllm_callback)
    subscribe_event(Event.ChatLLMStart, file_chatllm_callback)
    subscribe_event(Event.ChatLLMEnd, file_chatllm_callback)
    subscribe_event(Event.ToolStart, file_tool_callback)
    subscribe_event(Event.ToolEnd, file_tool_callback)
    subscribe_event(Event.AgentStep, file_agent_callback)
    subscribe_event(Event.AgentTimeout, file_agent_callback)
