import datetime

from attr import dataclass


@dataclass
class BotEntity:
    id: int
    botname: str
    owner_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
