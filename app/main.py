from fastapi import FastAPI

from app.api.v1.router import v1_api_router


def init():
    """
    Initialize the app.
    - Configure API
    - Configure routing paths
    """
    _app = FastAPI(
        title="marvel-user-comics-api",
        description="Service allows to save comics lists by users",
        version="0.1.0",
    )
    _app.include_router(
        v1_api_router,
        prefix="/api/v1",
    )
    return _app


app = init()
