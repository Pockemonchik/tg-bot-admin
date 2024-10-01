from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.bots.domain.bot_entity import BotEntity
from src.core.base_model import BaseModel

if TYPE_CHECKING:
    from src.users.infrastructure.models.user_model import UserModel


class BotModel(BaseModel):
    __tablename__ = "bots"
    botname: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["UserModel"] = relationship(back_populates="bots")

    def to_domain(self) -> BotEntity:
        return BotEntity(
            id=self.id,
            owner_id=self.owner_id,
            botname=self.botname,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return str(self.id) + self.botname
