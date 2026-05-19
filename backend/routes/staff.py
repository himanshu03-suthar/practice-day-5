from fastapi import APIRouter

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.get("/")
def get_staff():
    return {"msg": "All staff"}
