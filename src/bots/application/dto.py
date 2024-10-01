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
