"""JSON parser -> handles list-of-objects or single object. Uses utils.dict_to_metta for nested structures."""
import json
from .utils import dict_to_metta, sanitize_token

def parse_json(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lines = []
    if isinstance(data, list):
        for obj in data:
            if not isinstance(obj, dict):
                # primitive in top-level list -> create an entry per item
                entry_id = sanitize_token(str(obj))
                lines.append(f"(entry {entry_id})")
                lines.append(f"(value {entry_id} \"{str(obj)}\")")
            else:
                obj_lines, root_id = dict_to_metta(obj, None, id_prefix='item')
                lines.extend(obj_lines)
    elif isinstance(data, dict):
        obj_lines, root_id = dict_to_metta(data, None, id_prefix='root')
        lines.extend(obj_lines)
    else:
        # primitive
        entry_id = sanitize_token(str(data))
        lines.append(f"(entry {entry_id})")
        lines.append(f"(value {entry_id} \"{str(data)}\")")
    return lines
