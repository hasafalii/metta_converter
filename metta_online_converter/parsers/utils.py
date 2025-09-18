def sanitize_token(token: str) -> str:
    """Convert any string into a safe MeTTa token (alphanumeric + underscores)."""
    return "".join(c if c.isalnum() else "_" for c in token)

def format_value(value):
    """
    Wrap strings in quotes and keep numbers as-is.
    Converts None to empty string.
    """
    if value is None:
        return '""'
    try:
        float(value)
        return str(value)
    except ValueError:
        return f'"{value}"'
