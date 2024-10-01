import os
from datetime import datetime, timedelta, timezone

from dependency_injector.wiring import inject
from jose import jwt
from passlib.context import CryptContext

from src.users.application.dto import CreateUserDTO
from src.users.application.schemas import AuthUserShema, SuccessAuthUserShema
from src.users.application.user_service import UserService
from src.users.domain.errors import UserError


@inject
class AuthService:
    def __init__(
        self,
        user_service: UserService,
    ) -> None:
        self.user_service = user_service

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

    async def authenticate_user(self, creds: AuthUserShema):
        user = await self.user_service.get_users_by_username_or_none(username=creds.username)
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
        exist_user = await self.user_service.get_users_by_username_or_none(username=input_dto.username)
        if exist_user:
            raise UserError("User with this username already exist!")

        new_user = await self.user_service.create_user(
            CreateUserDTO(
                username=input_dto.username,
                password=self.get_password_hash(input_dto.password),
            )
        )
        return await self.user_service.authenticate_user(
            AuthUserShema(
                username=new_user.username,
                password=input_dto.password,
            )
        )
