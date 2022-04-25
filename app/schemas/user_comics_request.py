from typing import List

from pydantic import BaseModel


class UserComicsRequest(BaseModel):

    comics: List[int]
    token: str
