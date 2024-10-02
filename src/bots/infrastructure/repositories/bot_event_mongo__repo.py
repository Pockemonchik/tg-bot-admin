from datetime import datetime
from typing import Any, List

from bson import ObjectId
from pymongo.database import Database

from src.bots.application.dto import CreateBotEventEntityDTO, UpdateBotEventEntityDTO
from src.bots.domain.bot_event_entity import BotEventEntity
from src.bots.domain.bot_event_repo import IBotEventRepository
from src.bots.domain.errors import BotEventEntityError, BotEventEntityErrorNotFound


class BotEventEntityMongoRepository(IBotEventRepository):

    def __init__(self, db: Database):
        self._collection = db.get_collection("bot_events")

    @staticmethod
    def document_to_domain(document: dict):
        bot_event = BotEventEntity(**document)

        return bot_event

    async def get_one(self, id: str) -> BotEventEntity | Any:
        """Получение заметки по id"""
        print("get_1 mongo id", id)
        document = await self._collection.find_one({"_id": ObjectId(id)})

        if not document:
            raise BotEventEntityErrorNotFound(f"BotEventEntity with id={id} was not found!")

        document["id"] = str(document["_id"])
        del document["_id"]
        return self.document_to_domain(document)

    async def get_all(self) -> List[BotEventEntity] | None:
        """Получение всех заметок"""
        documents = await self._collection.find({}).to_list()

        for document in documents:
            document["id"] = str(document["_id"])
            del document["_id"]

        return [self.document_to_domain(document) for document in documents]

    async def add_one(self, new_bot_event: CreateBotEventEntityDTO) -> BotEventEntity | Any:
        """Добавление заметки, без тэгов"""
        document = new_bot_event.model_dump()
        document["created_at"] = datetime.now()
        document["updated_at"] = datetime.now()
        result = await self._collection.insert_one(document)

        return await self.get_one(id=result.inserted_id)

    async def update_one(self, id: str, bot_event_update: UpdateBotEventEntityDTO) -> BotEventEntity | Any:
        """Обновление заметки, без тэгов"""
        new_values = {"$set": bot_event_update.model_dump()}
        result = await self._collection.update_one({"_id": ObjectId(id)}, new_values)
        if result.modified_count == 1:
            return await self.get_one(id=id)
        else:
            raise BotEventEntityError(f"err when del")

    async def delete_one(self, id: str) -> int | None:
        """Удаление заметки, без тэгов"""
        result = await self._collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count

    async def filter_by_field(self, params: dict) -> List[BotEventEntity] | None:
        """Фильтр любому поллю кроме тэгов"""
        params = {key: value for (key, value) in params.items() if value != None}
        documents = await self._collection.find(params).to_list()

        for document in documents:
            document["id"] = str(document["_id"])
            del document["_id"]

        return [self.document_to_domain(document) for document in documents]

    async def filter_by_tag_name(self, tag_name: str) -> List[BotEventEntity] | None:
        """Фильтр заметок по тэгу"""
        documents = await self._collection.find({"tags": {"$in": [tag_name]}}).to_list()

        for document in documents:
            document["id"] = str(document["_id"])
            del document["_id"]

        return [self.document_to_domain(document) for document in documents]
