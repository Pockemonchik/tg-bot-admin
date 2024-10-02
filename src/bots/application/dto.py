import datetime

from pydantic import BaseModel


class BotDTO(BaseModel):
    id: int
    botname: str
    owner_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UpdateBotDTO(BaseModel):
    botname: str


class FilterBotDTO(BaseModel):
    id: int | None = None
    botname: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class CreateBotDTO(BaseModel):
    botname: str
    owner_id: int


class BotClientDTO(BaseModel):
    id: int
    name: str
    bot_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CreateBotClientDTO(BaseModel):
    name: str
    bot_id: int


class BotEventDTO(BaseModel):
    id: str
    bot_id: int
    bot_client_id: int
    type: str
    message: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CreateBotEventDTO(BaseModel):
    bot_id: int
    bot_client_id: int
    type: str
    message: str


class UpdateBotEventDTO(BaseModel):
    id: str
    bot_id: str
    bot_client_id: int
    type: str
    message: str
