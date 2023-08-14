from abc import ABC
import pickle
import inspect
from embedia.llm import LLM
from embedia.message import Message
from embedia.utils.pubsub import publish_event


class ChatLLM(ABC):
    """Abstract class for chat based LLMs.

    For LLMs that have a next token generation based interface, use the LLM class.

    Arguments:
    ----------
    - `system_prompt`: The first message in the chat history with a `system` role
    which defines the overall behaviour of the chatbot.

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

    pandas_expert = OpenAIChatLLM("You are an expert in writing commands for the python pandas library. Write one-line commands to solve the user's problems")
    msg = await openai_chatllm(Message(role='user', content='I want to extract all the pincodes in the column "address" and create another column "pincode"'))
    print(msg.content)

    >>> df['pincode'] = df['address'].str.extract(r'(\\d{6})')
    """

    def __init__(self, system_prompt: str):
        publish_event('chatllm_init', data={'system_prompt': system_prompt})
        self.chat_history = [Message(role='system', content=system_prompt)]
        self.llm: LLM = None

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

    async def __call__(self, message: Message) -> Message:
        publish_event('chatllm_start', data={
                      'message_role': message.role, 'message_content': message.content})
        self.chat_history.append(message)
        if self.llm:
            prompt = ''
            for message in self.chat_history:
                prompt += "{}: {}\n".format(message.role, message.content)
            prompt += "assistant: "
            reply = await self.llm(prompt)
            reply = Message(role='assistant', content=reply)
        else:
            argspec = inspect.getfullargspec(self._reply)
            arg_names = argspec.args
            if 'message' not in arg_names:
                raise ValueError("Argument: message not found in _reply definition")
            if set(arg_names) - {'self', 'message'}:
                raise ValueError("Only message argument is allowed in _reply definition")
            reply = await self._reply(message)
        self.chat_history.append(reply)
        publish_event('chatllm_end', data={
                      'reply_role': reply.role, 'reply_content': reply.content})
        return reply

    @classmethod
    def from_llm(cls, llm: LLM, system_prompt: str):
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
        instance = cls(system_prompt)
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
        raise NotImplementedError("Please implement _reply method in your ChatLLM subclass")
