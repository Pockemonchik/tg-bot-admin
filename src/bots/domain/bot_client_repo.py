from abc import ABC, abstractmethod
from typing import Any, List

from src.bots.application.dto import UpdateBotDTO
from src.bots.domain.bot_client_entity import BotClientEntity


class IBotClientRepository(ABC):
    @abstractmethod
    async def get_one(self, id: int) -> BotClientEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[BotClientEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, new_bot: BotClientEntity) -> BotClientEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, bot_update: UpdateBotDTO) -> BotClientEntity | Any:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def filter_by_field(self, field: str) -> List[BotClientEntity] | None:
        raise NotImplementedError
