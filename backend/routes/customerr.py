from fastapi import APIRouter

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.get("/")
def get_customers():
    return {"msg": "All customers"}