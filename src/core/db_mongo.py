import os

from pymongo import AsyncMongoClient, MongoClient
from pymongo.database import Database


def get_mongo_database() -> Database:
    connection_str = os.environ.get("MONGO_CONNECTION_URL", "mongodb://localhost:27017/")
    db_name = os.environ.get("MONGO_DATABASE_NAME", "example_app")

    mongo_client: MongoClient = MongoClient(connection_str, serverSelectionTimeoutMS=5)
    database = mongo_client.get_database(db_name)

    return database


def get_async_mongo_client() -> Database:
    connection_str = os.environ.get("MONGO_CONNECTION_URL", "mongodb://localhost:27017/")
    db_name = os.environ.get("MONGO_DATABASE_NAME", "example_app")

    mongo_client: AsyncMongoClient = AsyncMongoClient(connection_str, serverSelectionTimeoutMS=5)
    database = mongo_client.get_database(db_name)

    return database
