from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import os, shutil

from parsers.csv_parser import parse_csv
from parsers.json_parser import parse_json
from parsers.txt_parser import parse_txt
from parsers.web_parser import parse_website
from parsers.api_parser import parse_api

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

PARSERS = {
    "csv": parse_csv,
    "json": parse_json,
    "txt": parse_txt,
    "web": parse_website,
    "api": parse_api,
}

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert(
    request: Request,
    source_type: str = Form(...),
    file: UploadFile = None,
    url: str = Form(None)
):
    parser = PARSERS.get(source_type)
    if not parser:
        return {"error": f"Unsupported source type: {source_type}"}

    temp_input = None
    if file:
        temp_input = os.path.join(UPLOAD_DIR, file.filename)
        with open(temp_input, "wb") as f:
            shutil.copyfileobj(file.file, f)
    elif url:
        temp_input = url
    else:
        return {"error": "Provide a file or URL"}

    try:
        lines = parser(temp_input)
    except Exception as e:
        return {"error": str(e)}

    output_file = os.path.join(UPLOAD_DIR, f"{file.filename if file else 'output'}.metta")
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(line + "\n" for line in lines)

    return FileResponse(output_file, filename=os.path.basename(output_file))
