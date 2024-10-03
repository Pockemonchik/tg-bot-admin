from src.bots.application.dto import CreateBotDTO, UpdateBotDTO
from src.bots.domain.entities.bot_entity import BotEntity
from src.bots.domain.repositories.bot_repo import IBotRepository
from src.bots.infrastructure.models.bot_model import BotModel
from src.core.base_repo import BasePostgresRepository


class BotPostgresRepository(BasePostgresRepository, IBotRepository):
    model = BotModel
    entity = BotEntity
    create_dto = CreateBotDTO
    update_dto = UpdateBotDTO
