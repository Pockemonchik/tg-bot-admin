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


class UpdateBotClientDTO(BaseModel):
    name: str | None = None
    bot_id: int | None = None


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


class FilteBotEventDTO(BaseModel):
    bot_client_id: int | None = None
    type: str | None = None
    message: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class BotStatDTO(BaseModel):
    bot_id: int
    clients_count: int
    active_clients_count: int
    events_count: str
