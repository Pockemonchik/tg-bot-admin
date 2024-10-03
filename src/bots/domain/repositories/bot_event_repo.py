from abc import ABC, abstractmethod
from typing import Any, List

from src.bots.application.dto import UpdateBotEventDTO
from src.bots.domain.entities.bot_event_entity import BotEventEntity


class IBotEventRepository(ABC):
    @abstractmethod
    async def find_one(self, id: int) -> BotEventEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[BotEventEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, new_bot_event: BotEventEntity) -> BotEventEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, bot_event_update: UpdateBotEventDTO) -> BotEventEntity | Any:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def filter_by_field(self, field: str) -> List[BotEventEntity] | None:
        raise NotImplementedError
