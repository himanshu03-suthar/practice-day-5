from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()

class user(BaseModel):
    name:str
    age:int
    city:str
    add:str

@app.get("/")
def home():
    return{
        "message":"hello duniya"
    }

@app.post("/create")
def user_create():
    return{
        "message":"user created"
    }

@app.put("/update")
def user_update():
    return{
        "message":"user updated"
    }