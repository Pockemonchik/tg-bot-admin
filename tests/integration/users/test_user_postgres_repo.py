import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from src.users.application.dto import CreateUserDTO, UpdateUserDTO
from src.users.domain.user_entity import UserEntity
from src.users.infrastructure.user_postgres__repo import UserPostgresRepository


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
async def test_can_get_all_users(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = UserPostgresRepository(postgres_async_session)

    # when
    result = await repo.get_all()

    # then
    assert len(result) >= 3


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
async def test_can_get_one_user(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = UserPostgresRepository(postgres_async_session)

    # when
    result = await repo.get_one(id=1)

    # then
    assert type(result) == UserEntity
    assert result.id == 1


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
async def test_can_add_one_user(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = UserPostgresRepository(postgres_async_session)
    # создается без тэгов, логика их добавления в services
    data = {
        "username": "username",
        "password": "content",
    }

    new_user = CreateUserDTO(**data)
    # when
    result = await repo.add_one(new_user=new_user)
    print("add_one result", result)
    # then
    assert type(result) == UserEntity
    assert result.username == "username"


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
async def test_can_update_one_user(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = UserPostgresRepository(postgres_async_session)

    data = {
        "username": "username_updated",
        "password": "password_updated",
    }

    user_update = UpdateUserDTO(**data)
    # when
    result = await repo.update_one(id=1, user_update=user_update)

    # then
    assert type(result) == UserEntity
    assert result.username == "username_updated"


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
async def test_can_filter_by_fields(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = UserPostgresRepository(postgres_async_session)

    # when
    result = await repo.filter_by_field(
        {
            "username": "username_updated",
            "password": "password_updated",
        }
    )

    # then
    assert type(result) == list
    assert len(result) >= 1


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
async def test_can_delete_one_user(postgres_async_session: async_scoped_session[AsyncSession]) -> None:
    # given
    repo = UserPostgresRepository(postgres_async_session)

    # when
    result = await repo.delete_one(id=1)

    # then
    assert type(result) == int
    assert result == 1
