from abc import ABC, abstractmethod
from typing import Any, List, TypeVar

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_model import BaseModel as BaseSqlachemyModel
from src.core.errors import RepositoryError, ResourceNotFound


class AbstractRepository(ABC):
    """Base repo for all datasourses"""

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class BasePostgresRepository(AbstractRepository):
    """Base Postgres sqlachemy datasourses"""

    model: BaseSqlachemyModel = None
    entity = TypeVar("Entity")
    create_dto = TypeVar("Entity", bound="BaseModel")
    update_dto = TypeVar("Entity", bound="BaseModel")

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_one(self, id: int) -> entity | Any:
        obj: BaseSqlachemyModel = await self.session.get(
            self.model,
            id,
        )  # type: ignore
        await self.session.commit()
        if obj == None:
            await self.session.close()
            raise ResourceNotFound((f"Bot with id={id} was not found!"))
        else:
            await self.session.close()
            return obj.to_domain()

    async def find_all(self) -> List[entity] | None:
        stmt = select(self.model)  # type: ignore
        obj: BaseSqlachemyModel = await self.session.execute(stmt)
        await self.session.close()
        if obj:
            bot_list = [row[0].to_domain() for row in obj.unique().all()]
            return bot_list
        else:
            return None

    async def add_one(self, new_item: create_dto) -> entity | Any:
        try:
            new_bot_model: BaseSqlachemyModel = self.model(**new_item.model_dump())
            self.session.add(new_bot_model)  # type: ignore
            await self.session.commit()
            await self.session.close()
            return new_bot_model.to_domain()
        except DatabaseError as e:
            if isinstance(e, sqlalchemy.exc.IntegrityError):
                raise ResourceNotFound((f"{str(self.__class__)} was not found!"))
            else:
                raise RepositoryError

    async def update_one(self, id: int, update_data: update_dto) -> entity | Any:
        obj: BaseSqlachemyModel = await self.session.get(
            self.model,
            id,
        )  # type: ignore
        if obj == None:
            await self.session.close()
            raise ResourceNotFound((f"{str(self.__class__)} was not found!"))
        else:
            for name, value in update_data.model_dump().items():
                setattr(obj, name, value)
            result = obj.to_domain()
            await self.session.commit()
            await self.session.close()
            return result

    async def delete_one(self, id: int) -> int | None:
        obj: BaseSqlachemyModel = await self.session.get(
            self.model,
            int(id),
        )  # type: ignore
        await self.session.commit()
        if obj == None:
            await self.session.close()
            raise ResourceNotFound((f"{str(self.__class__)} was not found!"))

        else:
            # obj.tags = []
            await self.session.delete(obj)
            await self.session.commit()
            await self.session.close()
            return id

    async def filter_by_field(self, params: dict) -> List[entity] | None:
        filters = []
        for key, value in params.items():
            if value != None:
                filters.append(getattr(self.model, key) == value)
        stmt = select(self.model).filter(*filters)
        obj = await self.session.execute(stmt)
        await self.session.commit()
        if obj:
            bot_list = [row[0].to_domain() for row in obj.unique().all()]
            return bot_list
        else:
            return None
