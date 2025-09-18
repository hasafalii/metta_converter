#!/usr/bin/env bash
# Setup script for MeTTa Converter project

set -e

echo ">>> Creating virtual environment (.venv)"
python3 -m venv .venv

echo ">>> Activating virtual environment"
# Works for Linux/Mac
source .venv/bin/activate || true
# Works for Windows PowerShell
if [ -f ".venv/Scripts/activate" ]; then
  . .venv/Scripts/activate
fi

echo ">>> Upgrading pip"
pip install --upgrade pip

echo ">>> Installing dependencies"
pip install -r requirements.txt

echo ">>> Installation complete!"
echo "Run the converter like this:"
echo "    source .venv/bin/activate    # (Linux/Mac)"
echo "    .venv\\Scripts\\activate     # (Windows PowerShell)"
echo "    python converter.py csv examples/example.csv output.metta"
