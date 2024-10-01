import os
from datetime import datetime, timedelta, timezone
from typing import List

from dependency_injector.wiring import inject
from jose import jwt
from passlib.context import CryptContext

from src.users.application.dto import CreateUserDTO, UserDTO
from src.users.application.schemas import AuthUserShema, SuccessAuthUserShema
from src.users.domain.errors import UserError
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

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        auth_data = {
            "secret_key": os.environ.get(
                "SECRET_KEY",
                "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt",
            ),
            "algorithm": os.environ.get(
                "ALGORITHM",
                "HS256",
            ),
        }
        encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])
        return encode_jwt

    @staticmethod
    def get_password_hash(password: str) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)

    # Auth

    async def authenticate_user(self, creds: AuthUserShema):
        user = await self.get_users_by_username_or_none(username=creds.username)
        if not user:
            raise UserError("User with this username not found!")
        if not self.verify_password(
            plain_password=creds.password,
            hashed_password=user.password,
        ):
            raise UserError("Wrong password")
        access_token = self.create_access_token({"sub": str(user.id)})
        return SuccessAuthUserShema(id=user.id, username=user.username, token=access_token)

    async def register_user(self, input_dto: CreateUserDTO) -> None:
        exist_user = await self.get_users_by_username_or_none(username=input_dto.username)
        if exist_user:
            raise UserError("User with this username already exist!")

        new_user = await self.create_user(
            CreateUserDTO(
                username=input_dto.username,
                password=self.get_password_hash(input_dto.password),
            )
        )
        return await self.authenticate_user(
            AuthUserShema(
                username=new_user.username,
                password=input_dto.password,
            )
        )

    # Crud

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

    async def get_users_by_username_or_none(self, username: str) -> UserEntity | None:
        users = await self.get_users_by_filter({"username": username})
        if not users:
            return None
        return users[0]
