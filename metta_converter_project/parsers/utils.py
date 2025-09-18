"""Utility helpers for building MeTTa expressions from Python data structures."""
from typing import Any, List, Tuple
import uuid
import itertools
import re

_counter = itertools.count(1)

def _short_id():
    return uuid.uuid4().hex[:8]

def make_id(prefix: str = "obj") -> str:
    # deterministic-ish readable id
    return f"{prefix}_{next(_counter)}_{_short_id()}"

def sanitize_token(token: str) -> str:
    if token is None:
        return ''
    # Replace whitespace and illegal chars with underscore
    s = re.sub(r"\s+", "_", str(token))
    s = re.sub(r"[^A-Za-z0-9_\-\.:]", "_", s)
    return s

def format_value(value: Any) -> str:
    # Numbers and booleans -> raw; everything else -> quoted with escaped quotes
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return str(value)
    # Strings and others
    s = str(value)
    s = s.replace('"', '\\"')
    return f'"{s}"'

def dict_to_metta(obj: dict, obj_id: str = None, id_prefix='obj') -> Tuple[List[str], str]:
    """Convert a dictionary into MeTTa lines.

    Returns (lines, root_id) where lines is a list of expressions and root_id is the id assigned to this dict.
    """
    lines = []
    if obj_id is None:
        obj_id = make_id(id_prefix)
    lines.append(f"(entry {sanitize_token(obj_id)})")

    for k, v in obj.items():
        k_token = sanitize_token(k)
        if isinstance(v, dict):
            child_lines, child_id = dict_to_metta(v, None, id_prefix=k_token)
            lines.extend(child_lines)
            lines.append(f"({k_token} {sanitize_token(obj_id)} {sanitize_token(child_id)})")
        elif isinstance(v, list):
            # For lists, create child items or primitives
            for idx, item in enumerate(v, start=1):
                if isinstance(item, (dict, list)):
                    child_lines, child_id = dict_to_metta(item, None, id_prefix=k_token)
                    lines.extend(child_lines)
                    lines.append(f"({k_token} {sanitize_token(obj_id)} {sanitize_token(child_id)})")
                else:
                    val = format_value(item)
                    lines.append(f"({k_token} {sanitize_token(obj_id)} {val})")
        else:
            val = format_value(v)
            lines.append(f"({k_token} {sanitize_token(obj_id)} {val})")
    return lines, obj_id
