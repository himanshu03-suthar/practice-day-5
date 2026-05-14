from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

appointments: List[dict] = []

class Appointment(BaseModel):
    name: str
    phone: str
    service: str
    stylist: str
    date: str
    time: str

@app.get("/")
def home():
    return {
        "message": "The salon booking service is running"
    }

@app.post("/book")
def book_appointment(data: Appointment):
    appointment = data.dict()
    appointments.append(appointment)

    return {
        "message": "Your appointment booking was successful",
        "appointment": appointment
    }

@app.get("/appointments")
def get_appointments():
    return appointments