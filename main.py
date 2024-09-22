from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Store submissions in memory (for demonstration)
submissions = []

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
async def submit_form(
    image: UploadFile,
    name: str = Form(...),
    contact: str = Form(...),
    erp: str = Form(...),
    branch: str = Form(...),
    semester: int = Form(...),
    email: str = Form(...),
    college: str = Form(...)
):
    submissions.append({
        "image": image.filename,
        "name": name,
        "contact": contact,
        "erp": erp,
        "branch": branch,
        "semester": semester,
        "email": email,
        "college": college,
    })
    return {"message": "Submission successful!"}

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "submissions": submissions})
