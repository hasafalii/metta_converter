"""Plain text parser: each line becomes a MeTTa (line n "content") expression."""
from .utils import format_value

def parse_txt(file_path: str):
    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, raw in enumerate(f, start=1):
                content = raw.rstrip('\n')
                lines.append(f"(line_{i} {format_value(content)})")
    except FileNotFoundError:
        raise
    return lines
