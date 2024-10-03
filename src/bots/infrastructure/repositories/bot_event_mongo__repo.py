from datetime import datetime
from typing import Any, List

from bson import ObjectId
from pymongo.database import Database

from src.bots.application.dto import CreateBotEventDTO, UpdateBotEventDTO
from src.bots.domain.entities.bot_event_entity import BotEventEntity
from src.bots.domain.errors import BotEventErrorNotFound
from src.bots.domain.repositories.bot_event_repo import IBotEventRepository


class BotEventMongoRepository(IBotEventRepository):

    def __init__(self, db: Database):
        self._collection = db.get_collection("bot_events")

    @staticmethod
    def document_to_domain(document: dict):
        bot_event = BotEventEntity(**document)

        return bot_event

    async def find_one(self, id: str) -> BotEventEntity | Any:
        print("get_1 mongo id", id)
        document = await self._collection.find_one({"_id": ObjectId(id)})

        if not document:
            raise BotEventErrorNotFound(f"BotEventEntity with id={id} was not found!")

        document["id"] = str(document["_id"])
        del document["_id"]
        return self.document_to_domain(document)

    async def find_all(self) -> List[BotEventEntity] | None:
        """Получение всех заметок"""
        documents = await self._collection.find({}).to_list()

        for document in documents:
            document["id"] = str(document["_id"])
            del document["_id"]

        return [self.document_to_domain(document) for document in documents]

    async def add_one(self, new_item: CreateBotEventDTO) -> BotEventEntity | Any:
        document = new_item.model_dump()
        document["created_at"] = datetime.now()
        document["updated_at"] = datetime.now()
        result = await self._collection.insert_one(document)

        return await self.find_one(id=result.inserted_id)

    async def update_one(self, id: str, update_data: UpdateBotEventDTO) -> BotEventEntity | Any:
        new_values = {"$set": update_data.model_dump()}
        result = await self._collection.update_one({"_id": ObjectId(id)}, new_values)
        if result.modified_count == 1:
            return await self.find_one(id=id)
        else:
            raise BotEventErrorNotFound(f"err when del")

    async def delete_one(self, id: str) -> int | None:
        result = await self._collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count

    async def filter_by_field(
        self,
        params: dict,
        limit: int | None = 0,
        offset: int | None = 0,
    ) -> List[BotEventEntity] | None:
        params = {key: value for (key, value) in params.items() if value != None}
        documents = await self._collection.find(params).skip(offset).limit(limit).to_list()

        for document in documents:
            document["id"] = str(document["_id"])
            del document["_id"]

        return [self.document_to_domain(document) for document in documents]

    async def count_by_filter(self, params: dict) -> int | None:
        params = {key: value for (key, value) in params.items() if value != None}
        count = await self._collection.count_documents(params)
        return count
