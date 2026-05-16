from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Dict

app = FastAPI()

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

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

# 🔥 Put globals here
content_store: Dict[str, str] = {}

@app.get("/")
def home():
    return {"message": "CyberConnect backend running"}

@app.post("/contact")
def contact(form: ContactForm):
    print("New message received:")
    print(form)

    return {"message": "Message sent successfully!"}
