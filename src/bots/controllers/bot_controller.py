import json
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.bots.application.bot_client_service import BotClientService
from src.bots.application.bot_service import BotService
from src.bots.application.dto import BotClientDTO, BotDTO, CreateBotClientDTO, CreateBotDTO, FilterBotDTO, UpdateBotDTO
from src.core.errors import APIErrorMessage
from src.di import Container
from src.users.controllers.deps import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)],
)


# Read


@router.get(
    "/bots/",
    response_model=List[BotDTO],
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["bots"],
)
@inject
async def get_all(
    service: BotService = Depends(
        Provide[Container.bot_service],
    ),
) -> JSONResponse:
    result = await service.get_all_bots()
    json_result = [json.loads(item.model_dump_json()) for item in result]
    return JSONResponse(content=json_result, status_code=status.HTTP_200_OK)


@router.get(
    "/bots/filter/",
    response_model=List[BotDTO],
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["bots"],
)
@inject
async def get_filtered_bots(
    filter: FilterBotDTO = Depends(),
    service: BotService = Depends(
        Provide[Container.bot_service],
    ),
) -> JSONResponse:
    result = await service.get_bots_by_filter(filter.model_dump())
    json_result = [json.loads(item.model_dump_json()) for item in result]
    return JSONResponse(content=json_result, status_code=status.HTTP_200_OK)


@router.get(
    "/bots/{bot_id}",
    response_model=BotDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["bots"],
)
@inject
async def get_bot(
    bot_id: int,
    service: BotService = Depends(Provide[Container.bot_service]),
) -> JSONResponse:
    result = await service.get_bot_by_id(id=bot_id)
    return JSONResponse(
        content=json.loads(result.model_dump_json()),
        status_code=status.HTTP_200_OK,
    )


# Write


@router.post(
    "/bots/",
    response_model=BotDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["bots"],
)
@inject
async def create_bot(
    request: CreateBotDTO,
    service: BotService = Depends(
        Provide[Container.bot_service],
    ),
) -> JSONResponse:
    result = await service.create_bot(request)
    return JSONResponse(
        content=json.loads(result.model_dump_json()),
        status_code=status.HTTP_201_CREATED,
    )


@router.put(
    "/bots/{bot_id}",
    response_model=BotDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["bots"],
)
@inject
async def update_bot(
    request: UpdateBotDTO,
    bot_id: int,
    service: BotService = Depends(
        Provide[Container.bot_service],
    ),
) -> JSONResponse:
    result = await service.update_bot(id=bot_id, input_dto=request)
    return JSONResponse(
        content=json.loads(result.model_dump_json()),
        status_code=status.HTTP_201_CREATED,
    )


@router.delete(
    "/bots/{bot_id}",
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["bots"],
)
@inject
async def delete_bot(
    bot_id: int | str,
    service: BotService = Depends(Provide[Container.bot_service]),
) -> JSONResponse:
    result = await service.delete_bot(id=bot_id)
    return JSONResponse(
        content=(result),
        status_code=status.HTTP_200_OK,
    )


# Clients


@router.get(
    "/bots/{bot_id}/clients",
    response_model=BotClientDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["bot clients"],
)
@inject
async def get_bot_clients(
    bot_id: int,
    service: BotClientService = Depends(Provide[Container.bot_client_service]),
) -> JSONResponse:
    result = await service.get_bot_clients(bot_id=bot_id)
    json_result = [json.loads(item.model_dump_json()) for item in result]
    return JSONResponse(
        content=json_result,
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/bots/{bot_id}/clients",
    response_model=BotDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["bot clients"],
)
@inject
async def create_bot_client(
    request: CreateBotClientDTO,
    service: BotClientService = Depends(
        Provide[Container.bot_client_service],
    ),
) -> JSONResponse:
    result = await service.create_bot_client(request)
    return JSONResponse(
        content=json.loads(result.model_dump_json()),
        status_code=status.HTTP_201_CREATED,
    )
