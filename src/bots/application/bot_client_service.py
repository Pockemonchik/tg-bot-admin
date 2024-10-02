from dependency_injector.wiring import inject

from src.bots.application.dto import BotClientDTO, BotDTO, CreateBotDTO
from src.bots.domain.bot_client_entity import BotClientEntity
from src.bots.domain.bot_client_repo import IBotClientRepository


@inject
class BotClientService:
    def __init__(self, clients_repo: IBotClientRepository) -> None:
        self.clients_repo = clients_repo

    @staticmethod
    def bot_client_entity_to_dto(bot_client_entity_obj: BotClientEntity) -> BotClientDTO:
        bot_client_dict = vars(bot_client_entity_obj)
        bot_client_dto = BotClientDTO(**bot_client_dict)
        return bot_client_dto

    # Clients crud
    async def get_bot_clients(self, bot_id: int):
        clients = await self.clients_repo.filter_by_field({"bot_id": bot_id})
        dto_list = [self.bot_client_entity_to_dto(entity_obj) for entity_obj in clients]
        return dto_list

    async def create_bot_client(self, input_dto: CreateBotDTO) -> BotDTO:
        new_bot = await self.clients_repo.add_one(new_bot_client=input_dto)
        return self.bot_client_entity_to_dto(new_bot)

    async def update_bot_client(self, id: int, input_dto: CreateBotDTO) -> BotDTO:
        new_bot = await self.clients_repo.update_one(id=id, bot_client_update=input_dto)
        return self.bot_client_entity_to_dto(new_bot)

    async def delete_bot_client(self, id: int) -> int | None:
        result = await self.clients_repo.delete_one(id=id)
        return result

    # Bot Crud
