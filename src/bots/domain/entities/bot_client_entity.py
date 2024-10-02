import datetime

from attr import dataclass


@dataclass
class BotClientEntity:
    id: int
    bot_id: str
    name: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
