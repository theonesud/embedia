from embedia.utils.exceptions import MaxTokenError


def check_token_length(len_tokens: int, max_length: int):
    if len_tokens > max_length:
        raise MaxTokenError(f"Length of input text: {len_tokens} is longer than max_input_tokens: {max_length}")
