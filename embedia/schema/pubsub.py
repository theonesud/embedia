from enum import Enum


class Event(str, Enum):
    """The available events in the pubsub pipeline."""

    LLMStart = "LLM Start"
    LLMEnd = "LLM End"
    ChatLLMInit = "ChatLLM Init"
    ChatLLMStart = "ChatLLM Start"
    ChatLLMEnd = "ChatLLM End"
    ToolStart = "Tool Start"
    ToolEnd = "Tool End"
    EmbeddingStart = "Embedding Start"
    EmbeddingEnd = "Embedding End"
    AgentStart = "Agent Start"
    AgentStep = "Agent Step"
    AgentEnd = "Agent End"
    AgentTimeout = "Agent Timeout"
