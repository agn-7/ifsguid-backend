from fastapi import FastAPI

from .endpoints import router


def create_app() -> FastAPI:
    """
    Returns a FastAPI app object.
    """
    app = FastAPI(
        title="ifsguid", openapi_url="/api/openapi.json", version="0.1.0"
    )

    app.include_router(router, prefix="/api")
    return app


app = create_app()
