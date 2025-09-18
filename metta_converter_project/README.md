# MeTTa Converter (Python)

This project is a starter template for converting various data sources into `.metta` symbolic expression files.

## Features
- Parsers for CSV, JSON, XML, TXT, web pages (paragraphs) and generic JSON APIs.
- Nested objects are broken into sub-objects with generated IDs.
- Simple CLI using `converter.py`.

## Install
Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage
```bash
python converter.py csv examples/example.csv output.metta
python converter.py json examples/example.json output.metta
python converter.py xml examples/example.xml output.metta
python converter.py txt examples/example.txt output.metta
python converter.py web https://example.com output.metta
python converter.py api https://api.example.com/data output.metta
```

## Notes & Improvements
- The parsers are intentionally simple and readable. For production:
  - Add retry/backoff for network calls (requests + tenacity).
  - Respect robots.txt and rate limits for scraping.
  - Add tests and CI.
  - Consider streaming large CSV/JSON sources instead of loading everything into memory.
  - Add logging configuration and structured logs.
  - Add schema mapping to control how keys map to MeTTa predicates.
