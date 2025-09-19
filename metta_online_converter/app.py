from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
from parsers.csv_parser import parse_csv
from parsers.json_parser import parse_json
from parsers.txt_parser import parse_txt

app = FastAPI()

# --- Directories ---
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
METTA_FILES_DIR = "metta_files"
os.makedirs(METTA_FILES_DIR, exist_ok=True)

# --- Setup Static & Templates ---
app.mount(f"/{STATIC_DIR}", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# --- Parsers ---
PARSERS = {
    "csv": parse_csv,
    "json": parse_json,
    "txt": parse_txt,
}

# --- Helper Function ---
def save_metta_file(filename: str, content: list[str]):
    file_path = os.path.join(METTA_FILES_DIR, f"{filename}.metta")
    with open(file_path, "w", encoding="utf-8") as f:
        for line in content:
            f.write(line.rstrip() + "\n")

# --- Home / Converter Page ---
@app.get("/", response_class=HTMLResponse)
async def converter_page(request: Request):
    """Renders the main converter page directly (no login)."""
    return templates.TemplateResponse("index.html", {"request": request})

# --- Conversion Endpoint ---
@app.post("/convert")
async def convert(
    request: Request,
    source_type: str = Form(...),
    file: UploadFile = File(None),
):
    parser_fn = PARSERS.get(source_type)
    if not parser_fn:
        raise HTTPException(status_code=400, detail="Invalid source type")

    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse the file
        metta_lines = parser_fn(temp_file_path)
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        # Save converted file
        save_metta_file(file.filename, metta_lines)

        content = "\n".join(metta_lines)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during conversion: {e}")

    return HTMLResponse(content=f"<pre>{content}</pre>")
