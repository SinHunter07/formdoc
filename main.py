from fastapi import FastAPI, UploadFile, Form , Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sqlalchemy.orm import Session
from database import Submission, SessionLocal, init_db
import os
from pathlib import Path

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    college: str = Form(...),
    db: Session = Depends(get_db)
):
    # Save the uploaded image
    file_location = UPLOAD_DIR / image.filename
    with open(file_location, "wb") as buffer:
        buffer.write(await image.read())

    submission = Submission(
        image=image.filename,
        name=name,
        contact=contact,
        erp=erp,
        branch=branch,
        semester=semester,
        email=email,
        college=college,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return {"message": "Submission successful!"}



@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, db: Session = Depends(get_db)):
    submissions = db.query(Submission).all()
    return templates.TemplateResponse("admin.html", {"request": request, "submissions": submissions})

