from typing import Optional, List

from pydantic import BaseModel


class UserComicsResponse(BaseModel):

    saved_comics: Optional[List[int]]
    duplicated_comics: Optional[List[int]]
