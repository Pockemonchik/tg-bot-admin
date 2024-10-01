from typing import List

from dependency_injector.wiring import inject

from src.bots.application.dto import BotDTO, CreateBotDTO
from src.bots.domain.bot_entity import BotEntity
from src.bots.domain.bot_repo import IBotRepository


@inject
class BotService:
    def __init__(
        self,
        repo: IBotRepository,
    ) -> None:
        self.repo = repo

    @staticmethod
    def bot_entity_to_dto(bot_entity_obj: BotEntity) -> BotDTO:
        bot_dict = vars(bot_entity_obj)
        bot_dto = BotDTO(**bot_dict)
        return bot_dto

    # Crud

    async def create_bot(self, input_dto: CreateBotDTO) -> BotDTO:
        new_bot = await self.repo.add_one(new_bot=input_dto)
        return self.bot_entity_to_dto(new_bot)

    async def update_bot(self, id: int, input_dto: CreateBotDTO) -> BotDTO:
        new_bot = await self.repo.update_one(id=id, bot_update=input_dto)
        return self.bot_entity_to_dto(new_bot)

    async def get_bot_by_id(self, id: int) -> BotDTO:
        bot_entity_obj = await self.repo.get_one(id=id)
        bot_dto = self.bot_entity_to_dto(bot_entity_obj)
        return bot_dto

    async def get_all(self) -> List[BotDTO]:
        notes = await self.repo.get_all()
        bot_dto_list = [self.bot_entity_to_dto(bot_entity_obj) for bot_entity_obj in notes]
        return bot_dto_list

    async def delete_bot(self, id: int) -> int | None:
        result = await self.repo.delete_one(id=id)
        return result

    async def get_bots_by_filter(self, params: dict) -> List[BotEntity] | None:
        notes = await self.repo.filter_by_field(params)
        bot_dto_list = [self.bot_entity_to_dto(bot_entity_obj) for bot_entity_obj in notes]
        return bot_dto_list

    async def get_bots_by_botname_or_none(self, botname: str) -> BotEntity | None:
        bots = await self.get_bots_by_filter({"botname": botname})
        if not bots:
            return None
        return bots[0]
