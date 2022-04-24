from fastapi import APIRouter

router = APIRouter()


@router.post("")
def save_comics():
    return "success"
