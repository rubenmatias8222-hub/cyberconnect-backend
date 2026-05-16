from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
app = FastAPI()

# Allow frontend access (good security practice)
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

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL_ADDRESS,
    MAIL_PASSWORD=EMAIL_PASSWORD,
    MAIL_FROM=EMAIL_ADDRESS,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

# Email sending function
async def send_email(name: str, email: str, message: str):
    msg = MessageSchema(
        subject="New Contact Form Message",
        recipients=[EMAIL_ADDRESS],  # YOU receive it
        body=f"""
New Contact Form Submission:

Name: {name}
Email: {email}
Message:
{message}
""",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(msg)

@app.get("/")
def home():
    return {"message": "CyberConnect backend running"}

# Contact endpoint (NOW sends email)
@app.post("/contact")
async def contact(form: ContactForm):

    await send_email(
        form.name,
        form.email,
        form.message
    )

    return {
        "message": "Message sent successfully!"
    }
