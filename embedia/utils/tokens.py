
def check_token_length(len_tokens: int, max_length: int):
    if len_tokens > max_length:
        raise ValueError(f"Length of input text: {len_tokens} token(s) is longer than max_input_tokens: {max_length}")
