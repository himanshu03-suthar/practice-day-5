from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import booking, staff, customer
from routes.todos import router as todos_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(booking.router)
app.include_router(staff.router)
app.include_router(customer.router)
app.include_router(todos_router)

@app.get("/")
def home():
    return {"message": "Salon Booking API Running 🚀"}