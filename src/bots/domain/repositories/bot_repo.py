from abc import ABC, abstractmethod
from typing import Any, List

from src.bots.application.dto import UpdateBotDTO
from src.bots.domain.entities.bot_entity import BotEntity


class IBotRepository(ABC):
    @abstractmethod
    async def get_one(self, id: int) -> BotEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[BotEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, new_bot: BotEntity) -> BotEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, bot_update: UpdateBotDTO) -> BotEntity | Any:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def filter_by_field(self, params: dict) -> List[BotEntity] | None:
        raise NotImplementedError
