import datetime

from pydantic import BaseModel

from src.bots.application.dto import BotDTO


class UserDTO(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    bots: list[BotDTO]


class UpdateUserDTO(BaseModel):
    username: str
    password: str


class FilterUserDTO(BaseModel):
    id: int | None = None
    username: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class CreateUserDTO(BaseModel):
    username: str
    password: str
