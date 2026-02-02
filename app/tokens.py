import math

AVG_CHARS_PER_TOKEN = 4  # fallback

def tokens_from_usage(resp_json: dict) -> int:
    """
    Пытаемся взять точные токены из ответа GigaChat.
    Если usage отсутствует — fallback на estimate.
    """
    usage = resp_json.get("usage")
    if isinstance(usage, dict) and "total_tokens" in usage:
        return int(usage.get("total_tokens", 0))
    return 0


def estimate_tokens(messages, response_text: str) -> int:
    total_chars = 0
    for m in messages:
        total_chars += len(m.get("content", "") or "")
    total_chars += len(response_text or "")
    return max(1, math.ceil(total_chars / AVG_CHARS_PER_TOKEN))
