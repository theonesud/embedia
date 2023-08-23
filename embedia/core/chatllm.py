import pickle
from abc import ABC
from typing import Optional

from embedia.core.llm import LLM
from embedia.core.tokenizer import Tokenizer
from embedia.schema.message import Message
from embedia.utils.pubsub import publish_event
from embedia.utils.tokens import check_token_length
from embedia.utils.exceptions import DefinitionError


class ChatLLM(ABC):
    """Abstract class for chat based LLMs.

    For LLMs that have a next token generation based interface, use the LLM class.

    Arguments:
    ----------
    - `system_prompt`: The first message in the chat history with a `system` role
    which defines the overall behaviour of the chatbot.
    - `tokenizer`: An object of the `Tokenizer` class used for counting number of tokens.
    - `max_input_tokens`: The maximum number of tokens allowed in the input message.

    Methods:
    --------
    - `_reply()`: Implement this method to return the reply to the user's message.
    - `__call__()`: This method will call the _reply() internally.
    - `save_chat()`: Save the chat history to a file.
    - `load_chat()`: Load the chat history from a file.
    - `from_llm()`: Create a ChatLLM instance from an LLM instance.

    Example:
    --------
    ```
    class OpenAIChatLLM(ChatLLM):
        async def _reply(self, message: Message) -> Message:
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[message.to_json() for message in self.chat_history],
            )
            return Message(**completion.choices[0].message)

    class OpenAITokenizer(Tokenizer):
        async def _tokenize(self, text):
            return tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text)

    pandas_expert = OpenAIChatLLM("You are an expert in writing commands for the python pandas library. Write one-line commands to solve the user's problems",
                                  OpenAITokenizer(), 4096)
    msg = await openai_chatllm(Message(role='user', content='I want to extract all the pincodes in the column "address" and create another column "pincode"'))
    print(msg.content)

    >>> df['pincode'] = df['address'].str.extract(r'(\\d{6})')
    """

    def __init__(self, tokenizer: Tokenizer, max_input_tokens: int, system_prompt: Optional[str] = None) -> None:
        if system_prompt:
            self.set_system_prompt(system_prompt)
        else:
            self.chat_history = []
        self.llm: LLM = None
        self.tokenizer = tokenizer
        self.max_input_tokens = max_input_tokens

    def set_system_prompt(self, system_prompt: str) -> None:
        """
        Clears the chat history and sets the system prompt.

        Arguments:
        ----------
        - `system_prompt`: The first message in the chat history with a `system` role which defines the overall behaviour of the chatbot.

        Example:
        --------
        ```
        chatllm.set_system_prompt('You are an expert in writing commands for the python pandas library. Write one-line commands to solve the user's problems')
        """
        publish_event('chatllm_init', data={'system_prompt': system_prompt})
        self.chat_history = [Message(role='system', content=system_prompt)]

    def save_chat(self, filepath: str) -> None:
        """Save the chat history to a file.

        Arguments:
        ----------
        - `filepath`: The path to the file where the chat history will be saved.

        Example:
        --------
        ```
        chatllm.save_chat('temp/chatllm.pkl')
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self.chat_history, f)
        publish_event('chatllm_saved', data={'filepath': filepath})

    def load_chat(self, filepath: str) -> None:
        """Load the chat history from a file.

        Arguments:
        ----------
        - `filepath`: The path to the file from where the chat history will be loaded.

        Example:
        --------
        ```
        chatllm.load_chat('temp/chatllm.pkl')
        """
        with open(filepath, 'rb') as f:
            self.chat_history = pickle.load(f)
        publish_event('chatllm_loaded', data={'filepath': filepath})

    async def _call_llm(self, message: Message) -> Message:
        prompt = ''
        for message in self.chat_history:
            prompt += "{}: {}\n".format(message.role, message.content)
        prompt += "assistant: "
        reply = await self.llm(prompt)
        reply = Message(role='assistant', content=reply)
        return reply

    async def _call_chatllm(self, message: Message) -> Message:
        tokens = self.tokenizer(message.content)
        # TODO: should probably check the token length of the entire history
        check_token_length(tokens, self.max_input_tokens)
        publish_event('chatllm_start', data={
            'message_role': message.role, 'message_content': message.content,
            'num_tokens': len(tokens)})

        reply = await self._reply(message)

        if not isinstance(reply, Message):
            raise DefinitionError(f"_reply output must be of type: Message, got: {type(reply)}")

        tokens = self.tokenizer(reply.content)
        publish_event('chatllm_end', data={
            'reply_role': reply.role, 'reply_content': reply.content,
            'num_tokens': len(tokens), 'chat_history': self.chat_history})

        return reply

    async def __call__(self, message: Message, meta_prompting=False) -> Message:
        if not self.chat_history:
            raise DefinitionError("Please set the system prompt using the set_system_prompt method or pass it in the constructor")
        if not isinstance(message, Message):
            raise DefinitionError(f"Input must be of type: Message, got: {type(message)}")

        if meta_prompting:
            pass
            # send prompt to a prompt generator with the system message

        self.chat_history.append(message)
        if self.llm:
            reply = await self._call_llm(message)
        else:
            reply = await self._call_chatllm(message)
        self.chat_history.append(reply)

        return reply

    @classmethod
    def from_llm(cls, llm: LLM, system_prompt: Optional[str] = None) -> 'ChatLLM':
        """Create a ChatLLM instance from an LLM instance.

        Arguments:
        ----------
        - `llm`: The LLM instance.
        - `system_prompt`: The first message in the chat history with a `system` role which defines the overall behaviour of the chatbot.

        Returns:
        --------
        - `instance`: The ChatLLM instance.

        Example:
        --------
        ```
        openai_llm = OpenAILLM()
        openai_chatllm = ChatLLM.from_llm(openai_llm, SYSTEM_PROMPT)
        """
        instance = cls(llm.tokenizer, llm.max_input_tokens, system_prompt)
        instance.llm = llm
        return instance

    async def _reply(self, message: Message) -> Message:
        """This function calls the chat based LLM with the message and returns the reply.

        Use the __call__ method of the ChatLLM object to call this method. Do not call this method directly.

        Arguments:
        ----------
        - `message`: The message of Message type to be passed to the chat based LLM.

        Returns:
        --------
        - `reply`: The reply of Message type.
        """
        raise NotImplementedError
