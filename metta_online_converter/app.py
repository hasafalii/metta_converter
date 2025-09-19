from fastapi import FastAPI, Request, Form, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
from parsers.csv_parser import parse_csv
from parsers.json_parser import parse_json
from parsers.api_parser import parse_api
from parsers.xml_parser import parse_xml
from parsers.txt_parser import parse_txt
from parsers.web_parser import parse_website

app = FastAPI()

# --- Constants ---
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
METTA_FILES_DIR = "metta_files"
LOGIN_PASSWORD = "letmein123"

# --- Setup ---
os.makedirs(METTA_FILES_DIR, exist_ok=True)
app.mount(f"/{STATIC_DIR}", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# --- Parsers ---
PARSERS = {
    "csv": parse_csv,
    "json": parse_json,
    "xml": parse_xml,
    "txt": parse_txt,
    "web": parse_website,
    "api": parse_api,
}

# --- Helper Functions ---
def save_metta_file(filename: str, content: list[str]):
    """Saves the converted MeTTa content to a file."""
    file_path = os.path.join(METTA_FILES_DIR, f"{filename}.metta")
    with open(file_path, "w", encoding="utf-8") as f:
        for line in content:
            f.write(line.rstrip() + "\n")

# --- Login Routes ---
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Renders the login page."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    """Handles the login form submission."""
    if password == LOGIN_PASSWORD:
        response = RedirectResponse(url="/converter", status_code=302)
        response.set_cookie(key="access_granted", value="true")
        return response
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid password"}
    )

# --- Converter Route ---
@app.get("/converter", response_class=HTMLResponse)
async def converter_page(request: Request):
    """Renders the main converter page."""
    if request.cookies.get("access_granted") != "true":
        return RedirectResponse(url="/")
    return templates.TemplateResponse("index.html", {"request": request})

# --- Conversion Route ---
@app.post("/convert")
async def convert(
    request: Request,
    source_type: str = Form(...),
    url: str = Form(None),
    file: UploadFile = File(None),
):
    """Handles the file conversion."""
    if request.cookies.get("access_granted") != "true":
        return RedirectResponse(url="/")

    parser_fn = PARSERS.get(source_type)
    if not parser_fn:
        raise HTTPException(status_code=400, detail="Invalid source type")

    try:
        if file and file.filename:
            # Save the uploaded file temporarily
            temp_file_path = f"temp_{file.filename}"
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Parse the file
            metta_lines = parser_fn(temp_file_path)
            
            # Clean up the temporary file
            os.remove(temp_file_path)
            
            # Save the converted MeTTa file
            save_metta_file(file.filename, metta_lines)
            
            content = "\n".join(metta_lines)
        elif url:
            metta_lines = parser_fn(url)
            save_metta_file(url.replace("/", "_").replace(":", ""), metta_lines)
            content = "\n".join(metta_lines)
        else:
            raise HTTPException(status_code=400, detail="No file or URL provided")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during conversion: {e}")

    return HTMLResponse(content=f"<pre>{content}</pre>")