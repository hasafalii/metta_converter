"""Generic API parser: GET JSON and reuse json parsing logic when possible."""
import requests
import json
from .utils import dict_to_metta, sanitize_token, format_value

def parse_api(url: str):
    headers = {'User-Agent': 'metta-converter/1.0 (+https://example.com)'}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    lines = []
    if isinstance(data, dict):
        obj_lines, root_id = dict_to_metta(data, None, id_prefix='api')
        lines.extend(obj_lines)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                obj_lines, root_id = dict_to_metta(item, None, id_prefix='api_item')
                lines.extend(obj_lines)
            else:
                # primitive items
                eid = sanitize_token(str(item))
                lines.append(f"(entry {eid})")
                lines.append(f"(value {eid} {format_value(item)})")
    else:
        eid = sanitize_token(str(data))
        lines.append(f"(entry {eid})")
        lines.append(f"(value {eid} {format_value(data)})")
    return lines
