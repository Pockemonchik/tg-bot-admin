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
        bot_event_repo: IBotEventRepository,
        bot_repo: IBotRepository,
    ) -> None:
        self.bot_event_repo = bot_event_repo
        self.bot_repo = bot_repo

    @staticmethod
    def event_entity_to_dto(event_entity_obj: BotEventEntity) -> BotEventDTO:
        event_dict = vars(event_entity_obj)
        event_dto = BotEventDTO(**event_dict)
        return event_dto

    # BotEvent Crud

    # Read

    async def create_bot_event(self, bot_id: int, input_dto: CreateBotEventDTO) -> BotEventDTO:
        bot_entity_obj = await self.bot_repo.find_one(id=bot_id)
        input_dto.bot_id = bot_entity_obj.id
        new_event = await self.bot_event_repo.add_one(new_item=input_dto)
        return self.event_entity_to_dto(new_event)

    async def update_bot_event(self, id: int, input_dto: CreateBotEventDTO) -> BotEventDTO:
        new_event = await self.bot_event_repo.update_one(id=id, update_data=input_dto)
        return self.event_entity_to_dto(new_event)

    async def delete_bot_event(self, id: int) -> int | None:
        result = await self.bot_event_repo.delete_one(id=id)
        return result

    # Write

    async def get_bot_event_by_id(self, id: int) -> BotEventDTO:
        event_entity_obj = await self.bot_event_repo.find_one(id=id)
        event_dto = self.event_entity_to_dto(event_entity_obj)
        return event_dto

    async def get_bot_events_by_bot_id(
        self,
        bot_id: int,
        limit: int | None = 0,
        offset: int | None = 0,
        filters: dict | None = {},
    ) -> List[BotEventDTO]:
        query_params = dict({"bot_id": bot_id}, **filters)
        events = await self.bot_event_repo.filter_by_field(query_params, limit=limit, offset=offset)
        event_dto_list = [self.event_entity_to_dto(event_entity_obj) for event_entity_obj in events]
        return event_dto_list

    async def get_bot_events_by_filter(
        self,
        params: dict,
        limit: int | None = 0,
        offset: int | None = 0,
    ) -> List[BotEventEntity] | None:
        events = await self.bot_event_repo.filter_by_field(params=params, limit=limit, offset=offset)
        event_dto_list = [self.event_entity_to_dto(event_entity_obj) for event_entity_obj in events]
        return event_dto_list
