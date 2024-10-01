import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.core.errors import APIErrorMessage
from src.users.application.dto import CreateUserDTO, UserDTO
from src.users.application.schemas import AuthUserShema
from src.users.application.user_service import UserService
from src.users.di import UserContainer as Container

router = APIRouter()


# Auth


@router.post(
    "/register/",
    response_model=UserDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["auth"],
)
@inject
async def register_user(
    request: CreateUserDTO, service: UserService = Depends(Provide[Container.auth_service])
) -> JSONResponse:
    result = await service.register_user(request)
    return JSONResponse(content=json.loads(result.model_dump_json()), status_code=status.HTTP_201_CREATED)


@router.post(
    "/auth/",
    response_model=UserDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["auth"],
)
@inject
async def auth_user(
    request: AuthUserShema, service: UserService = Depends(Provide[Container.auth_service])
) -> JSONResponse:
    result = await service.authenticate_user(request)
    return JSONResponse(content=json.loads(result.model_dump_json()), status_code=status.HTTP_201_CREATED)
