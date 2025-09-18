from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from parsers.csv_parser import parse_csv
from parsers.json_parser import parse_json
from parsers.api_parser import parse_api

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Login password
LOGIN_PASSWORD = "letmein123"

# --- LOGIN ROUTES ---
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    if password == LOGIN_PASSWORD:
        response = RedirectResponse(url="/converter", status_code=302)
        response.set_cookie(key="access_granted", value="true")
        return response
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid password"}
    )

# --- CONVERTER ROUTE ---
@app.get("/converter", response_class=HTMLResponse)
async def converter_page(request: Request):
    if request.cookies.get("access_granted") != "true":
        return RedirectResponse(url="/")
    return templates.TemplateResponse("index.html", {"request": request})

# --- POST /convert ---
@app.post("/convert")
async def convert(request: Request, source_type: str = Form(...), url: str = Form(None)):
    if request.cookies.get("access_granted") != "true":
        return RedirectResponse(url="/")
    # Example placeholder logic
    content = f"; MeTTa conversion placeholder for {source_type} {url or 'file'}"
    return HTMLResponse(content=content)
