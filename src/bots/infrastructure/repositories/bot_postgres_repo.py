from sqlite3 import DatabaseError
from typing import Any, List

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bots.application.dto import CreateBotDTO, UpdateBotDTO
from src.bots.domain.bot_entity import BotEntity
from src.bots.domain.bot_repo import IBotRepository
from src.bots.domain.errors import BotErrorNotFound
from src.bots.infrastructure.models.bot_model import BotModel
from src.core.errors import RepositoryError


class BotPostgresRepository(IBotRepository):
    model = BotModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, id: int) -> BotEntity | Any:
        obj = await self.session.get(
            self.model,
            id,
        )  # type: ignore
        await self.session.commit()
        if obj == None:
            await self.session.close()
            raise BotErrorNotFound((f"Bot with id={id} was not found!"))
        else:
            await self.session.close()
            return obj.to_domain()

    async def get_all(self) -> List[BotEntity] | None:
        stmt = select(self.model)  # type: ignore
        obj = await self.session.execute(stmt)
        await self.session.close()
        if obj:
            bot_list = [row[0].to_domain() for row in obj.unique().all()]
            return bot_list
        else:
            return None

    async def add_one(self, new_bot: CreateBotDTO) -> BotEntity | Any:
        try:
            new_bot_model = self.model(**new_bot.model_dump())
            self.session.add(new_bot_model)  # type: ignore
            await self.session.commit()
            await self.session.close()
            return new_bot_model.to_domain()
        except DatabaseError as e:
            if isinstance(e, sqlalchemy.exc.IntegrityError):
                raise BotErrorNotFound((f"User with id={new_bot.owner_id} was not found!"))
            else:
                raise RepositoryError

    async def update_one(self, id: int, bot_update: UpdateBotDTO) -> BotEntity | Any:
        obj = await self.session.get(
            self.model,
            id,
        )  # type: ignore
        if obj == None:
            await self.session.close()
            raise BotErrorNotFound((f"Bot with id={id} was not found!"))
        else:
            for name, value in bot_update.model_dump().items():
                setattr(obj, name, value)
            result = obj.to_domain()
            await self.session.commit()
            await self.session.close()
            return result

    async def delete_one(self, id: int) -> int | None:
        obj = await self.session.get(
            self.model,
            int(id),
        )  # type: ignore
        await self.session.commit()
        if obj == None:
            await self.session.close()
            raise BotErrorNotFound((f"Bot with id={id} was not found!"))
        else:
            # obj.tags = []
            await self.session.delete(obj)
            await self.session.commit()
            await self.session.close()
            return id

    async def filter_by_field(self, params: dict) -> List[BotEntity] | None:
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
