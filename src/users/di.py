import os

from dependency_injector import containers, providers

from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.users.application.auth_service import AuthService
from src.users.application.user_service import UserService
from src.users.infrastructure.postgres_user_repo import UserPostgresRepository


class UserContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.users.controllers.auth_controller",
            "src.users.controllers.user_controller",
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

    posgtgres_repository = providers.Factory(
        UserPostgresRepository,
        session=async_session,
    )

    # Mongo inject

    repository = posgtgres_repository
    # Service inject
    # service = providers.Factory(UserService, user_repo=posgtgres_repository)
    user_service = providers.Factory(UserService, user_repo=repository)
    auth_service = providers.Factory(AuthService, user_service=user_service)
