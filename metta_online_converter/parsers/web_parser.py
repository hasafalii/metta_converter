import requests
from bs4 import BeautifulSoup
from parsers.utils import sanitize_token, format_value

def parse_website(url: str):
    lines = []
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch URL, status {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")

        for i, p in enumerate(paragraphs, start=1):
            para_id = sanitize_token(f"para_{i}")
            content = p.get_text(strip=True)
            if not content:
                continue
            val = format_value(content)
            lines.append(f"(paragraph {para_id} {val})")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Web request failed: {e}")

    return lines
