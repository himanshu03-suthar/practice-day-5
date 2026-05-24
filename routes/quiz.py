from fastapi import APIRouter

router=APIRouter()

@router.get("/")
def home():
    return{
        "message":"QUIZ ROUTES IS WORKING"
    }