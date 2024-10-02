from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.bots.domain.entities.bot_client_entity import BotClientEntity
from src.core.base_model import BaseModel

if TYPE_CHECKING:
    from src.bots.infrastructure.models.bot_model import BotModel


class BotClientModel(BaseModel):
    __tablename__ = "clients"
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    bot_id: Mapped[int] = mapped_column(ForeignKey("bots.id"))
    bot: Mapped["BotModel"] = relationship(back_populates="clients")

    def to_domain(self) -> BotClientEntity:
        return BotClientEntity(
            id=self.id,
            bot_id=self.bot_id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return str(self.id) + self.name
