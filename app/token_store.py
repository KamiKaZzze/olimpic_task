import threading
from pathlib import Path

TOKEN_FILE = Path("tokens_used.txt")
_lock = threading.Lock()


def _read_tokens() -> int:
    if not TOKEN_FILE.exists():
        return 0
    try:
        return int(TOKEN_FILE.read_text().strip())
    except ValueError:
        return 0


def _write_tokens(value: int):
    TOKEN_FILE.write_text(str(value))


def add_tokens(count: int) -> int:
    """
    Atomically add tokens and return new total
    """
    with _lock:
        total = _read_tokens()
        total += count
        _write_tokens(total)
        return total


def get_total_tokens() -> int:
    with _lock:
        return _read_tokens()
