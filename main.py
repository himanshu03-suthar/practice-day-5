from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()


model=ChatOpenAI(
    model="gpt-3.5-turbo",
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

    return{
        "response":"Backend successfully connected"
    }