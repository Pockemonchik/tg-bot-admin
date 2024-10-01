from typing import Any

import uvicorn
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.bots.controllers.bot_controller import router as bot_router
from src.core.errors import APIErrorMessage, DomainError, RepositoryError, ResourceNotFound
from src.di import Container
from src.users.controllers.auth_controller import router as auth_router
from src.users.controllers.user_controller import router as users_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(bot_router)
    container = Container()
    app.container = container
    return app


app = create_app()


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=f"Oops! {exc}")
    return JSONResponse(
        status_code=400,
        content=error_msg.model_dump(),
    )


@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request: Request, exc: ResourceNotFound) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=str(exc))
    return JSONResponse(status_code=404, content=error_msg.model_dump())


@app.exception_handler(RepositoryError)
async def repository_error_handler(request: Request, exc: RepositoryError) -> JSONResponse:
    error_msg = APIErrorMessage(
        type=exc.__class__.__name__, message="Oops! Something went wrong, please try again later..."
    )
    return JSONResponse(
        status_code=500,
        content=error_msg.model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    # or logger.error(f'{exc}')
    print(request, exc_str)
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema  # type: ignore

    openapi_schema = get_openapi(
        title="tg_bot_admin",
        version="1.0.0",
        description="",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema  # type: ignore


app.openapi = custom_openapi  # type: ignore

if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
