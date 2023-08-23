from embedia.utils.pubsub import subscribe_event
import os
import logging
import json


def file_chatllm_end_callback(data):
    logging.info('ChatLLM>' + json.dumps(data, indent=2))


def file_tool_end_callback(data):
    logging.info('Tool>' + json.dumps(data, indent=2))


def file_llm_end_callback(data):
    logging.info('LLM>' + json.dumps(data, indent=2))


def file_agent_step_callback(data):
    logging.info('Agent>' + json.dumps(data, indent=2))


def setup_file_callback():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="logs/backup.log",
    )
    subscribe_event('chatllm_end', file_chatllm_end_callback)
    subscribe_event('tool_end', file_tool_end_callback)
    subscribe_event('llm_end', file_llm_end_callback)
    subscribe_event('agent_step', file_agent_step_callback)
