"""CSV parser -> return list of MeTTa expression strings."""
import csv
from parsers.utils import sanitize_token, format_value  # absolute import

def parse_csv(file_path: str):
    lines = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames is None:
                return []

            first_col = reader.fieldnames[0]

            for row in reader:
                raw_id = row.get(first_col) or ''
                entry_id = sanitize_token(raw_id) if raw_id else sanitize_token(f"row_{reader.line_num}")
                lines.append(f"(entry {entry_id})")

                for col in reader.fieldnames:
                    value = row.get(col)
                    if value is None:
                        continue
                    token = sanitize_token(col)
                    val = format_value(value)
                    lines.append(f"({token} {entry_id} {val})")

    except FileNotFoundError:
        raise

    return lines
