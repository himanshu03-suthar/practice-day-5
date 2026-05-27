import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langchain_groq import ChatGroq
from pydantic import BaseModel

from routes.quiz import router as quiz_router

BASE_DIR = Path(__file__).resolve().parent
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI(title="NOVA AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router, prefix="/quiz", tags=["quiz"])

model = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8B-instant",
    temperature=0.9
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "ai_configured": model is not None,
    }


@app.get("/")
def serve_index():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/style.css")
def serve_css():
    return FileResponse(BASE_DIR / "style.css", media_type="text/css")


@app.get("/script.js")
def serve_js():
    return FileResponse(BASE_DIR / "script.js", media_type="application/javascript")


class ChatRequest(BaseModel):
    message: str


@app.post("/CHAT")
def chat(request: ChatRequest):
    if model is None:
        return {
            "response": (
                "groq_API_KEY set nahi hai. "
                "Project folder mein .env file banao aur key add karo."
            )
        }

    try:
        response = model.invoke(request.message)
        return {"response": response.content}
    except Exception as e:
        print("ERROR:", e)
        return {"response": f"Error aayi: {str(e)}"}

