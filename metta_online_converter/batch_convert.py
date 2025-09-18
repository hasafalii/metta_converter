import os
import argparse
from parsers.csv_parser import parse_csv
from parsers.json_parser import parse_json
from parsers.txt_parser import parse_txt
from parsers.web_parser import parse_website
from parsers.api_parser import parse_api

PARSERS = {
    "csv": parse_csv,
    "json": parse_json,
    "txt": parse_txt,
    "web": parse_website,
    "api": parse_api,
}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def convert_source(source_type, input_path, output_file=None):
    parser = PARSERS.get(source_type)
    if not parser:
        print(f"[ERROR] Unsupported source type: {source_type}")
        return

    try:
        lines = parser(input_path)
    except Exception as e:
        print(f"[ERROR] Failed to convert {input_path}: {e}")
        return

    if not output_file:
        base_name = os.path.basename(input_path) if os.path.isfile(input_path) else "output"
        output_file = os.path.join(UPLOAD_DIR, f"{base_name}.metta")

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(line + "\n" for line in lines)

    print(f"[SUCCESS] Created: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Batch convert files/URLs to MeTTa format.")
    parser.add_argument("source_type", choices=PARSERS.keys(), help="Type of source: csv, json, txt, web, api")
    parser.add_argument("inputs", nargs="+", help="Files or URLs to convert")
    parser.add_argument("--output_dir", default=UPLOAD_DIR, help="Directory to save .metta files")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for inp in args.inputs:
        output_file = os.path.join(args.output_dir, f"{os.path.basename(inp)}.metta")
        convert_source(args.source_type, inp, output_file)

if __name__ == "__main__":
    main()
