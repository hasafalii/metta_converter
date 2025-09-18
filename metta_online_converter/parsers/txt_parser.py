from parsers.utils import sanitize_token, format_value

def parse_txt(file_path: str):
    lines = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                content = line.strip()
                if not content:
                    continue
                line_id = sanitize_token(f"line_{i}")
                val = format_value(content)
                lines.append(f"(line {line_id} {val})")
    except FileNotFoundError:
        raise
    return lines
