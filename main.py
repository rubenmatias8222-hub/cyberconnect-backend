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

# Create database tables
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
# DEPENDENCY
# ---------------------------
# Yields a database session and guarantees it closes after the request finishes
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

# CONTACT (SAVE)
@app.post("/contact")
def contact(form: ContactForm, db: Session = Depends(get_db)):
    new_message = Message(
        name=form.name,
        email=form.email,
        message=form.message
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message) # Optional: updates new_message with its generated ID

    return {
        "status": "success",
        "user": form.name,
        "received": True,
        "message": "Saved to database"
    }

# GET MESSAGES (ADMIN VIEW)
@app.get("/messages")
def get_messages():
    db = SessionLocal()

    messages = db.query(Message).all()

    db.close()

    return [
        {
            "id": m.id,
            "name": m.name,
            "email": m.email,
            "message": m.message
        }
        for m in messages
    ]
