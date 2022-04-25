from functools import lru_cache

from pydantic import BaseSettings


class MarvelSearchSettings(BaseSettings):

    marvel_search_url: str


@lru_cache()
def get_marvel_search_settings():
    return MarvelSearchSettings()
