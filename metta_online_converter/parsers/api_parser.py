import requests
from parsers.utils import sanitize_token, format_value

def parse_api(url: str):
    lines = []
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API request failed, status {response.status_code}")

        data = response.json()
        if isinstance(data, dict):
            data = [data]

        for i, obj in enumerate(data):
            entry_id = sanitize_token(str(obj.get("id", f"api_obj_{i}")))
            lines.append(f"(entry {entry_id})")
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    continue
                token = sanitize_token(k)
                val = format_value(v)
                lines.append(f"({token} {entry_id} {val})")

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

    return lines
