from fastapi import APIRouter

router = APIRouter(prefix="/booking", tags=["Booking"])

@router.get("/")
def get_bookings():
    return {"msg": "All bookings"}