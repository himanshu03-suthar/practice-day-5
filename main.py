from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()

model=ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.9
)


@app.get("/")
def home():
    return{
        "message":"hello i am himanshu  how can i help you"
    }

class chatRequest(BaseModel):
    message:str

@app.post("/CHAT")
def chat(request:chatRequest):

    print(request.message)

    response=model.invoke(request.message)

    return{
        "response":response.content
    }
