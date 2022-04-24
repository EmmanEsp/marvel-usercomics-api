from fastapi import APIRouter, status

from app.api.v1.endpoints import user_comic

v1_api_router = APIRouter()

v1_api_router.include_router(
    user_comic.router,
    tags=["User Comics"],
    prefix="/addToLayaway",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
