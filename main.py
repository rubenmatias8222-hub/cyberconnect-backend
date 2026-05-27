from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.models import Message
from app.data.store import content_store

# ---------------------------
# INIT APP
# ---------------------------
app = FastAPI()

Base.metadata.create_all(bind=engine)

# ---------------------------
# CORS
# ---------------------------
origins = [
    "https://rubenmatias8222-hub.github.io",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# DB DEPENDENCY
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# MODELS
# ---------------------------
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContentUpload(BaseModel):
    title: str
    content: str

# ---------------------------
# ROUTES
# ---------------------------
@app.get("/")
def home():
    return {"message": "CyberConnect backend running"}

# SAVE MESSAGE
@app.post("/contact")
def contact(form: ContactForm, db: Session = Depends(get_db)):
    new_message = Message(
        name=form.name,
        email=form.email,
        message=form.message
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return {
        "status": "success",
        "message": "Saved to database"
    }

# GET MESSAGES (ADMIN DASHBOARD)
@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()

    return [
        {
            "id": m.id,
            "name": m.name,
            "email": m.email,
            "message": m.message
        }
        for m in messages
    ]

# CONTENT STORE (optional)
@app.get("/content")
def get_content():
    return content_store
