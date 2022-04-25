from fastapi import APIRouter

from app.schemas.user_comics_request import UserComicsRequest
from app.schemas.user_comics_response import UserComicsResponse
from app.services.user_comics_service import save_user_comics

router = APIRouter()


@router.post(
    "",
    response_model=UserComicsResponse,
    response_model_exclude_unset=True,
)
def save_comics(user_comics: UserComicsRequest):
    return save_user_comics(user_comics=user_comics)
