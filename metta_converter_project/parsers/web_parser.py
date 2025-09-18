"""Web page parser: extracts <p> paragraphs using requests + BeautifulSoup."""
import requests
from bs4 import BeautifulSoup
from .utils import format_value, sanitize_token

def parse_website(url: str):
    headers = {'User-Agent': 'metta-converter/1.0 (+https://example.com)'}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    paragraphs = soup.find_all('p')
    lines = []
    for i, p in enumerate(paragraphs, start=1):
        text = p.get_text(separator=' ', strip=True)
        if not text:
            continue
        pid = sanitize_token(f"p_{i}")
        lines.append(f"(paragraph {pid} {format_value(text)})")
    return lines
