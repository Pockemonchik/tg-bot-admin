from typing import List

from dependency_injector.wiring import inject

from src.bots.application.dto import BotDTO, BotStatsDTO, CreateBotDTO
from src.bots.domain.entities.bot_entity import BotEntity
from src.bots.domain.repositories.bot_client_repo import IBotClientRepository
from src.bots.domain.repositories.bot_event_repo import IBotEventRepository
from src.bots.domain.repositories.bot_repo import IBotRepository


@inject
class BotService:
    def __init__(
        self,
        bot_repo: IBotRepository,
        bot_client_repo: IBotClientRepository,
        bot_event_repo: IBotEventRepository,
    ) -> None:
        self.bot_repo = bot_repo
        self.bot_client_repo = bot_client_repo
        self.bot_event_repo = bot_event_repo

    @staticmethod
    def bot_entity_to_dto(bot_entity_obj: BotEntity) -> BotDTO:
        bot_dict = vars(bot_entity_obj)
        bot_dto = BotDTO(**bot_dict)
        return bot_dto

    # Bot stats
    async def get_bot_statictic(self, bot_id: int) -> BotStatsDTO:
        clients_count = await self.bot_client_repo.count_by_filter({"bot_id": bot_id})
        events_count = await self.bot_event_repo.count_by_filter({"bot_id": bot_id})
        result = BotStatsDTO(
            bot_id=bot_id,
            clients_count=clients_count,
            events_count=events_count,
        )
        return result
        # active_clients_count
        # events_count

    # Bot Crud

    # Read

    async def create_bot(self, input_dto: CreateBotDTO) -> BotDTO:
        new_bot = await self.bot_repo.add_one(new_item=input_dto)
        return self.bot_entity_to_dto(new_bot)

    async def update_bot(self, id: int, input_dto: CreateBotDTO) -> BotDTO:
        new_bot = await self.bot_repo.update_one(id=id, update_data=input_dto)
        return self.bot_entity_to_dto(new_bot)

    async def delete_bot(self, id: int) -> int | None:
        result = await self.bot_repo.delete_one(id=id)
        return result

    # Write

    async def get_bot_by_id(self, id: int) -> BotDTO:
        bot_entity_obj = await self.bot_repo.find_one(id=id)
        bot_dto = self.bot_entity_to_dto(bot_entity_obj)
        return bot_dto

    async def find_all_bots(self) -> List[BotDTO]:
        notes = await self.bot_repo.find_all()
        bot_dto_list = [self.bot_entity_to_dto(bot_entity_obj) for bot_entity_obj in notes]
        return bot_dto_list

    async def get_bots_by_filter(self, params: dict) -> List[BotEntity] | None:
        notes = await self.bot_repo.filter_by_field(params)
        bot_dto_list = [self.bot_entity_to_dto(bot_entity_obj) for bot_entity_obj in notes]
        return bot_dto_list

    async def get_bots_by_botname_or_none(self, botname: str) -> BotEntity | None:
        bots = await self.get_bots_by_filter({"botname": botname})
        if not bots:
            return None
        return bots[0]
