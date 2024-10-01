from typing import List

from dependency_injector.wiring import inject

from src.users.application.dto import CreateUserDTO, UserDTO
from src.users.domain.user_entity import UserEntity
from src.users.domain.user_repo import IUserRepository


@inject
class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
    ) -> None:
        self.user_repo = user_repo

    @staticmethod
    def user_entity_to_dto(user_entity_obj: UserEntity) -> UserDTO:

        user_dict = vars(user_entity_obj)
        user_dto = UserDTO(**user_dict)
        return user_dto

    async def create_user(self, input_dto: CreateUserDTO) -> UserDTO:
        new_user = await self.user_repo.add_one(new_user=input_dto)
        return self.user_entity_to_dto(new_user)

    async def update_user(self, id: int, input_dto: CreateUserDTO) -> UserDTO:
        new_user = await self.user_repo.update_one(id=id, user_update=input_dto)
        return self.user_entity_to_dto(new_user)

    async def get_user_by_id(self, id: int) -> UserDTO:
        user_entity_obj = await self.user_repo.get_one(id=id)
        user_dto = self.user_entity_to_dto(user_entity_obj)
        return user_dto

    async def get_all(self) -> List[UserDTO]:
        notes = await self.user_repo.get_all()
        user_dto_list = [self.user_entity_to_dto(user_entity_obj) for user_entity_obj in notes]
        return user_dto_list

    async def delete_user(self, id: int) -> int | None:
        result = await self.user_repo.delete_one(id=id)
        return result

    async def get_users_by_filter(self, params: dict) -> List[UserEntity] | None:
        notes = await self.user_repo.filter_by_field(params)
        user_dto_list = [self.user_entity_to_dto(user_entity_obj) for user_entity_obj in notes]
        return user_dto_list
