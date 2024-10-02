from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base_model import BaseModel
from src.users.domain.user_entity import UserEntity

if TYPE_CHECKING:
    from src.bots.infrastructure.models.bot_model import BotModel


class UserModel(BaseModel):
    __tablename__ = "users"
    username: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    bots: Mapped[List["BotModel"]] = relationship(back_populates="owner", lazy="subquery")

    def to_domain(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
            bots=[bot.to_domain() for bot in self.bots] if self.bots != [] else [],
        )

    def __str__(self) -> str:
        return str(self.id) + self.username
