import datetime

from attr import dataclass


@dataclass
class BotEventEntity:
    id: str
    bot_id: int
    bot_client_id: int
    type: str
    message: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
