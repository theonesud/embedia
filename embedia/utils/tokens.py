from embedia.utils.exceptions import MaxTokenError


def check_token_length(tokens, max_length):
    if len(tokens) > max_length:
        raise MaxTokenError(f"Length of input text: {len(tokens)} is longer than max_input_tokens: {max_length}")
