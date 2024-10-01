import nest_asyncio
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_postgres import AsyncPostgresDatabaseManager
from src.main import app
from src.users.application.user_service import UserService
from src.users.infrastructure.postgres_user_repo import UserPostgresRepository

nest_asyncio.apply()


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
async def async_test_client():
    db = AsyncPostgresDatabaseManager(
        url="postgresql+asyncpg://tg_bot_admin:tg_bot_admin@127.0.0.1:5436/tg_bot_admin",
        echo=True,
    )
    async_session = db.get_scoped_session()

    posgtgres_repository = UserPostgresRepository(session=async_session)

    service = UserService(user_repo=posgtgres_repository)
    app.container.service.override(service)
    with app.container.repository.override(posgtgres_repository):
        async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
            yield client


@pytest.fixture(scope="module")
def test_db_manager() -> AsyncPostgresDatabaseManager:
    db = AsyncPostgresDatabaseManager(
        url="postgresql+asyncpg://tg_bot_admin:tg_bot_admin@127.0.0.1:5436/tg_bot_admin",
        echo=True,
    )
    return db


@pytest.fixture(scope="module")
def postgres_async_session(test_db_manager) -> AsyncSession:
    return test_db_manager.get_scoped_session()
