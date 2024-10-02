import os

from dependency_injector import containers, providers
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from src.bots.application.services.bot_client_service import BotClientService
from src.bots.application.services.bot_event_service import BotEventService
from src.bots.application.services.bot_service import BotService
from src.bots.infrastructure.repositories.bot_client_postgres_repo import BotClientPostgresRepository
from src.bots.infrastructure.repositories.bot_event_mongo__repo import BotEventMongoRepository
from src.bots.infrastructure.repositories.bot_postgres_repo import BotPostgresRepository
from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.users.application.auth_service import AuthService
from src.users.application.user_service import UserService
from src.users.infrastructure.user_postgres__repo import UserPostgresRepository


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.users.controllers.auth_controller",
            "src.users.controllers.user_controller",
            "src.bots.controllers.bot_controller",
        ]
    )  # or "users" in your case

    # Define configuration
    config = providers.Configuration()

    # DBs
    db = AsyncPostgresDatabaseManager(
        url=os.environ.get("DB_URL", "postgresql+asyncpg://tg_bot_admin:tg_bot_admin@127.0.0.1:5436/tg_bot_admin"),
        echo=bool(os.environ.get("DB_ECHO", False)),
    )
    async_session = providers.Factory(
        db.get_scoped_session,
    )

    async_mongo_client = providers.Factory(
        AsyncMongoClient,
        "mongodb://localhost:27017/",
    )

    async_mongo_db = providers.Factory(
        AsyncDatabase,
        client=async_mongo_client,
        name="tg_bot_admin",
    )

    # users
    user_posgtgres_repository = providers.Factory(
        UserPostgresRepository,
        session=async_session,
    )
    user_service = providers.Factory(UserService, user_repo=user_posgtgres_repository)
    auth_service = providers.Factory(AuthService, user_service=user_service)

    # bots
    bot_posgtgres_repository = providers.Factory(
        BotPostgresRepository,
        session=async_session,
    )

    bot_service = providers.Factory(
        BotService,
        bot_repo=bot_posgtgres_repository,
    )

    # clients
    bot_client_posgtgres_repository = providers.Factory(
        BotClientPostgresRepository,
        session=async_session,
    )
    bot_client_service = providers.Factory(
        BotClientService,
        clients_repo=bot_client_posgtgres_repository,
    )

    # events
    bot_event_mongo_repository = providers.Factory(
        BotEventMongoRepository,
        db=async_mongo_db,
    )

    bot_event_service = providers.Factory(
        BotEventService,
        event_repo=bot_event_mongo_repository,
        bot_repo=bot_posgtgres_repository,
    )
