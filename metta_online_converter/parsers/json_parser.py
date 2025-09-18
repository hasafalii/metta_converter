import json
from parsers.utils import sanitize_token, format_value

def parse_json(file_path: str):
    lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            data = [data]

        for i, obj in enumerate(data):
            entry_id = sanitize_token(str(obj.get("id", f"obj_{i}")))
            lines.append(f"(entry {entry_id})")
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    continue
                token = sanitize_token(k)
                val = format_value(v)
                lines.append(f"({token} {entry_id} {val})")
    return lines
