from typing import List

from dependency_injector.wiring import inject

from src.bots.application.dto import BotEventDTO, CreateBotEventDTO
from src.bots.domain.entities.bot_event_entity import BotEventEntity
from src.bots.domain.repositories.bot_event_repo import IBotEventRepository
from src.bots.domain.repositories.bot_repo import IBotRepository


@inject
class BotEventService:
    def __init__(
        self,
        event_repo: IBotEventRepository,
        bot_repo: IBotRepository,
    ) -> None:
        self.event_repo = event_repo
        self.bot_repo = bot_repo

    @staticmethod
    def event_entity_to_dto(event_entity_obj: BotEventEntity) -> BotEventDTO:
        event_dict = vars(event_entity_obj)
        event_dto = BotEventDTO(**event_dict)
        return event_dto

    # BotEvent Crud

    # Read

    async def create_bot_event(self, bot_id: int, input_dto: CreateBotEventDTO) -> BotEventDTO:
        bot_entity_obj = await self.bot_repo.get_one(id=bot_id)
        input_dto.bot_id = bot_entity_obj.id
        new_event = await self.event_repo.add_one(new_bot_event=input_dto)
        return self.event_entity_to_dto(new_event)

    async def update_bot_event(self, id: int, input_dto: CreateBotEventDTO) -> BotEventDTO:
        new_event = await self.event_repo.update_one(id=id, bot_event_update=input_dto)
        return self.event_entity_to_dto(new_event)

    async def delete_bot_event(self, id: int) -> int | None:
        result = await self.event_repo.delete_one(id=id)
        return result

    # Write

    async def get_bot_event_by_id(self, id: int) -> BotEventDTO:
        event_entity_obj = await self.event_repo.get_one(id=id)
        event_dto = self.event_entity_to_dto(event_entity_obj)
        return event_dto

    async def get_all_bot_events(self, bot_id: int) -> List[BotEventDTO]:
        notes = await self.event_repo.filter_by_field({"bot_id": bot_id})
        event_dto_list = [self.event_entity_to_dto(event_entity_obj) for event_entity_obj in notes]
        return event_dto_list

    async def get_bot_events_by_filter(self, params: dict) -> List[BotEventEntity] | None:
        notes = await self.event_repo.filter_by_field(params)
        event_dto_list = [self.event_entity_to_dto(event_entity_obj) for event_entity_obj in notes]
        return event_dto_list

    # async def get_bot_events_by_eventname_or_none(self, botname: str) -> BotEventEntity | None:
    #     bots = await self.get_events_by_filter({"botname": botname})
    #     if not bots:
    #         return None
    #     return bots[0]
