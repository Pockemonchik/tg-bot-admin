from abc import ABC, abstractmethod
from typing import Any, List

from src.users.application.dto import UpdateUserDTO
from src.users.domain.user_entity import UserEntity


class IBotRepository(ABC):
    @abstractmethod
    async def get_one(self, id: int) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, new_user: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, user_update: UpdateUserDTO) -> UserEntity | Any:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    async def filter_by_field(self, field: str) -> List[UserEntity] | None:
        raise NotImplementedError
