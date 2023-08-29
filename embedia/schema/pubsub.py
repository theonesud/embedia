from enum import Enum


class Event(str, Enum):
    LLMStart = 'llm_start'
    LLMEnd = 'llm_end'
    ChatLLMInit = 'chatllm_init'
    ChatLLMStart = 'chatllm_start'
    ChatLLMEnd = 'chatllm_end'
    ToolStart = 'tool_start'
    ToolEnd = 'tool_end'
    EmbeddingStart = 'embedding_start'
    EmbeddingEnd = 'embedding_end'
    AgentStep = 'agent_step'
    AgentTimeout = 'agent_timeout'
