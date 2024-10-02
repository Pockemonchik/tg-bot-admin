import os

from dependency_injector import containers, providers

from src.bots.application.bot_service import BotService
from src.bots.infrastructure.postgres_bot_repo import BotPostgresRepository
from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.users.application.auth_service import AuthService
from src.users.application.user_service import UserService
from src.users.infrastructure.postgres_user_repo import UserPostgresRepository


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

    # Postgres inject
    db = AsyncPostgresDatabaseManager(
        url=os.environ.get("DB_URL", "postgresql+asyncpg://tg_bot_admin:tg_bot_admin@127.0.0.1:5436/tg_bot_admin"),
        echo=bool(os.environ.get("DB_ECHO", False)),
    )
    async_session = providers.Factory(
        db.get_scoped_session,
    )

    user_posgtgres_repository = providers.Factory(
        UserPostgresRepository,
        session=async_session,
    )

    bot_posgtgres_repository = providers.Factory(
        BotPostgresRepository,
        session=async_session,
    )

    user_service = providers.Factory(UserService, user_repo=user_posgtgres_repository)
    auth_service = providers.Factory(AuthService, user_service=user_service)
    bot_service = providers.Factory(BotService, repo=bot_posgtgres_repository)
