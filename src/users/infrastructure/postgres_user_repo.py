from typing import Any, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.application.dto import CreateUserDTO, UpdateUserDTO
from src.users.domain.errors import UserErrorNotFound
from src.users.domain.user_entity import UserEntity
from src.users.domain.user_repo import IUserRepository
from src.users.infrastructure.models.user_model import UserModel


class UserPostgresRepository(IUserRepository):
    model = UserModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, id: int) -> UserEntity | Any:
        obj = await self.session.get(
            self.model,
            id,
        )  # type: ignore
        await self.session.commit()
        if obj == None:
            await self.session.close()
            raise UserErrorNotFound((f"User with id={id} was not found!"))
        else:
            await self.session.close()
            return obj.to_domain()

    async def get_all(self) -> List[UserEntity] | None:
        stmt = select(self.model)  # type: ignore
        obj = await self.session.execute(stmt)
        await self.session.close()
        if obj:
            user_list = [row[0].to_domain() for row in obj.unique().all()]
            return user_list
        else:
            return None

    async def add_one(self, new_user: CreateUserDTO) -> UserEntity | Any:
        new_user_model = self.model(**new_user.model_dump())
        self.session.add(new_user_model)  # type: ignore
        await self.session.commit()
        await self.session.close()
        return new_user_model.to_domain()

    async def update_one(self, id: int, user_update: UpdateUserDTO) -> UserEntity | Any:
        obj = await self.session.get(
            self.model,
            id,
        )  # type: ignore
        if obj == None:
            await self.session.close()
            raise UserErrorNotFound((f"User with id={id} was not found!"))
        else:
            for name, value in user_update.model_dump().items():
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
            raise UserErrorNotFound((f"User with id={id} was not found!"))
        else:
            # obj.tags = []
            await self.session.delete(obj)
            await self.session.commit()
            await self.session.close()
            return id

    async def filter_by_field(self, params: dict) -> List[UserEntity] | None:
        filters = []
        for key, value in params.items():
            if value != None:
                filters.append(getattr(self.model, key) == value)
        stmt = select(self.model).filter(*filters)
        obj = await self.session.execute(stmt)
        await self.session.commit()
        if obj:
            user_list = [row[0].to_domain() for row in obj.unique().all()]
            return user_list
        else:
            return None
