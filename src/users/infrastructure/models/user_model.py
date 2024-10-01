from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel
from src.users.domain.user_entity import UserEntity


class UserModel(BaseModel):
    __tablename__ = "users"
    username: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def to_domain(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return str(self.id) + self.username
