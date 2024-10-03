from src.bots.application.dto import CreateBotClientDTO, UpdateBotClientDTO
from src.bots.domain.entities.bot_client_entity import BotClientEntity
from src.bots.domain.repositories.bot_repo import IBotRepository
from src.bots.infrastructure.models.bot_client_model import BotClientModel
from src.core.base_repo import BasePostgresRepository


class BotClientPostgresRepository(BasePostgresRepository, IBotRepository):
    model = BotClientModel
    entity = BotClientEntity
    create_dto = CreateBotClientDTO
    update_dto = UpdateBotClientDTO
