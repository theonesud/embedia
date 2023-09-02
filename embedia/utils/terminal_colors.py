COLOR_MAPPING = {
    "red": "91",
    "green": "92",
    "yellow": "93",
    "blue": "94",
    "magenta": "95",
    "cyan": "96",
}


def colored(text: str, color: str) -> str:
    code = COLOR_MAPPING[color]
    return f"\033[{code}m{text}\033[0m"
