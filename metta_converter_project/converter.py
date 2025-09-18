#!/usr/bin/env python3
"""metta_converter: CLI to convert multiple data sources into .metta symbolic files.

Usage examples:
  python converter.py csv examples/example.csv output.metta
  python converter.py json examples/example.json output.metta
  python converter.py api https://api.example.com/data output.metta
  python converter.py web https://example.com output.metta
"""
import argparse
import sys
import os
from parsers.csv_parser import parse_csv
from parsers.json_parser import parse_json
from parsers.xml_parser import parse_xml
from parsers.txt_parser import parse_txt
from parsers.web_parser import parse_website
from parsers.api_parser import parse_api

PARSERS = {
    "csv": parse_csv,
    "json": parse_json,
    "xml": parse_xml,
    "txt": parse_txt,
    "web": parse_website,
    "api": parse_api,
}

def write_metta(lines, output_file):
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln.rstrip() + "\n")

def main():
    p = argparse.ArgumentParser(description="Convert various data sources into .metta files.")
    p.add_argument("source_type", choices=PARSERS.keys(), help="Type of source (csv, json, xml, txt, web, api)")
    p.add_argument("input_path", help="File path or URL")
    p.add_argument("output_file", help="Output .metta file path")
    args = p.parse_args()

    parser_fn = PARSERS.get(args.source_type)
    if parser_fn is None:
        print("Unknown source_type. Valid options:", ", ".join(PARSERS.keys()))
        sys.exit(2)

    print(f"Parsing {args.source_type} -> {args.input_path} ...")
    try:
        metta_lines = parser_fn(args.input_path)
    except Exception as e:
        print("Error while parsing:", e)
        sys.exit(1)

    if not metta_lines:
        print("Warning: parser returned no lines.")

    try:
        write_metta(metta_lines, args.output_file)
    except Exception as e:
        print("Failed to write output:", e)
        sys.exit(1)

    print("Successfully wrote", args.output_file)

if __name__ == '__main__':
    main()
