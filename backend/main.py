from fastapi import FastAPI
from routes import booking, staff, customer

app = FastAPI()

app.include_router(booking.router)
app.include_router(staff.router)
app.include_router(customer.router)

@app.get("/")
def home():
    return {"message": "Salon Booking API Running 🚀"}