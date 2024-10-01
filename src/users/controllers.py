import json
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.core.errors import APIErrorMessage
from src.users.application.dto import CreateUserDTO, FilterUserDTO, UpdateUserDTO, UserDTO
from src.users.application.user_service import UserService
from src.users.bootstrap import UserContainer as Container

router = APIRouter()


@router.get(
    "/users/{user_id}",
    response_model=UserDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["users"],
)
@inject
async def get_user(user_id: int, service: UserService = Depends(Provide[Container.service])) -> JSONResponse:
    result = await service.get_user_by_id(id=user_id)
    return JSONResponse(content=json.loads(result.model_dump_json()), status_code=status.HTTP_200_OK)


@router.post(
    "/users/",
    response_model=UserDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["users"],
)
@inject
async def create_user(
    request: CreateUserDTO, service: UserService = Depends(Provide[Container.service])
) -> JSONResponse:
    result = await service.create_user(request)
    return JSONResponse(content=json.loads(result.model_dump_json()), status_code=status.HTTP_201_CREATED)


@router.put(
    "/users/{user_id}",
    response_model=UserDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["users"],
)
@inject
async def update_user(
    request: UpdateUserDTO, user_id: int, service: UserService = Depends(Provide[Container.service])
) -> JSONResponse:
    result = await service.update_user(id=user_id, input_dto=request)
    return JSONResponse(content=json.loads(result.model_dump_json()), status_code=status.HTTP_201_CREATED)


@router.delete(
    "/users/{user_id}",
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["users"],
)
@inject
async def delete_user(user_id: int | str, service: UserService = Depends(Provide[Container.service])) -> JSONResponse:
    result = await service.delete_user(id=user_id)
    return JSONResponse(content=(result), status_code=status.HTTP_200_OK)


@router.get(
    "/users/",
    response_model=List[UserDTO],
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["users"],
)
@inject
async def get_all(
    service: UserService = Depends(
        Provide[Container.service],
    ),
) -> JSONResponse:
    result = await service.get_all()
    json_result = [json.loads(item.model_dump_json()) for item in result]
    return JSONResponse(content=json_result, status_code=status.HTTP_200_OK)


@router.get(
    "/users/filter/",
    response_model=List[UserDTO],
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["users"],
)
@inject
async def get_filtered_users(
    filter: FilterUserDTO = Depends(),
    service: UserService = Depends(
        Provide[Container.service],
    ),
) -> JSONResponse:
    result = await service.get_users_by_filter(filter.model_dump())
    json_result = [json.loads(item.model_dump_json()) for item in result]
    return JSONResponse(content=json_result, status_code=status.HTTP_200_OK)
