from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
from models import Booking

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/booking", tags=["Booking"])

class BookingCreate(BaseModel):
    customer_name: str
    phone: str
    booking_date: str
    service: str
    service_price: str
    stylist: str
    time: str
    note: Optional[str] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return [
        {
            "id": booking.id,
            "customer_name": booking.customer_name,
            "phone": booking.phone,
            "booking_date": booking.booking_date,
            "service": booking.service,
            "service_price": booking.service_price,
            "stylist": booking.stylist,
            "time": booking.time,
            "note": booking.note,
        }
        for booking in bookings
    ]

@router.post("/", status_code=201)
def create_booking(booking_in: BookingCreate, db: Session = Depends(get_db)):
    booking = Booking(
        customer_name=booking_in.customer_name,
        phone=booking_in.phone,
        booking_date=booking_in.booking_date,
        service=booking_in.service,
        service_price=booking_in.service_price,
        stylist=booking_in.stylist,
        time=booking_in.time,
        note=booking_in.note,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {
        "message": "Booking created successfully",
        "booking_id": booking.id,
    }
