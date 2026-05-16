from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
app = FastAPI()

# Allow frontend access
origins = [
    "https://rubenmatias8222-hub.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validation model
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.get("/")
def home():
    return {"message": "CyberConnect backend running"}

@app.post("/contact")
def contact(form: ContactForm):

    print("New message received:")
    print(form)

    return {
        "message": "Message sent successfully!"
    }
