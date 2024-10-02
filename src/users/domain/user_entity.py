import datetime
from typing import List

from attr import dataclass

from src.bots.domain.bot_entity import BotEntity


@dataclass
class UserEntity:
    id: int
    username: str
    password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    bots: List[BotEntity]
