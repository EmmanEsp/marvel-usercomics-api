from typing import List

import requests
from bson import ObjectId
from fastapi import HTTPException, status
from jose import jwt, JWTError

from app.infraestructure.mongodb_client import get_client
from app.schemas.user_comics_request import UserComicsRequest
from app.schemas.user_comics_response import UserComicsResponse
from app.settings.marvel_search_settings import get_marvel_search_settings
from app.settings.security_settings import get_security_settings


def _decode_jwt(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        secret_key = get_security_settings().secret_key
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"],
        )
        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception


def _validate_comic(comic_id: int):
    _base_url = get_marvel_search_settings()
    _resource = "validate_comic/"
    response = requests.get(f"{_base_url.marvel_search_url}{_resource}{comic_id}").json()
    return response["isValid"]


def save_user_comics(user_comics: UserComicsRequest):
    user_id = _decode_jwt(token=user_comics.token)

    for comic_id in user_comics.comics:
        is_valid = _validate_comic(comic_id)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Comic #{comic_id} is not a valid comic",
            )

    client = get_client()
    db = client.user

    user_comic_list = db.comics.find_one({"user_id": user_id})

    if not user_comic_list:
        db.comics.insert_one(
            {"user_id": user_id, "comic_list": user_comics.comics}
        )
        return UserComicsResponse(saved_comics=user_comics.comics)

    set_comics = set(user_comic_list["comic_list"])
    valid_comics = []
    duplicated_comics = []

    for comic_id in user_comics.comics:
        if comic_id in set_comics:
            duplicated_comics.append(comic_id)
        else:
            valid_comics.append(comic_id)

    if len(valid_comics) > 0:
        new_comics_list = [*valid_comics, *user_comic_list["comic_list"]]
        db.comics.update_one(
            {"_id": user_comic_list["_id"]},
            {
                "$set": {"comic_list": new_comics_list}
            }
        )

    return UserComicsResponse(
        saved_comics=valid_comics,
        duplicated_comics=duplicated_comics,
    )
