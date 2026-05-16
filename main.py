from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Dict

app = FastAPI()

# Allow frontend access
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
# STORAGE (UPLOAD SYSTEM)
# ---------------------------

content_store: Dict[str, str] = {}

# ---------------------------
# ROUTES
# ---------------------------

@app.get("/")
def home():
    return {"message": "CyberConnect backend running"}

# CONTACT FORM
@app.post("/contact")
def contact(form: ContactForm):

    print("New message received:")
    print(form)

    return {"message": "Message sent successfully!"}

# ---------------------------
# ADMIN UPLOAD SYSTEM
# ---------------------------

@app.post("/upload")
def upload_content(data: ContentUpload):

    content_store[data.title] = data.content

    return {
        "message": "Content uploaded successfully!",
        "title": data.title
    }

# ---------------------------
# GET CONTENT (FRONTEND USE)
# ---------------------------

@app.get("/content")
def get_content():

    return content_store
