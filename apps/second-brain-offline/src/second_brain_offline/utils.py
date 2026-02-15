import random
import string

import tiktoken

def merge_dicts(dict1: dict, dict2: dict) -> dict:
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dicts(result[key], value)
            elif isinstance(result[key], list) and isinstance(value, list):
                result[key] = result[key] + value
            else:
                result[key] = value
        else:
            result[key] = value

    return result

def generate_random_hex(length: int) -> str:
    hex_chars = string.hexdigits.lower()
    return "".join(random.choice(hex_chars) for _ in range(length))

def clip_tokens(text: str, max_tokens: int, model_id: str) -> str:
    try:
        encoding = tiktoken.encoding_for_model(model_id)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
    
    return encoding.decode(tokens[:max_tokens])