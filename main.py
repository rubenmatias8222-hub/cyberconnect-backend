from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "CyberConnect backend running"}

@app.post("/contact")
def contact(data: dict):
    return {
        "success": True,
        "message": "Message received",
        "data": data
    }
