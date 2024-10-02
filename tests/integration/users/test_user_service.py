import pytest

from src.users.application.dto import CreateUserDTO, UpdateUserDTO, UserDTO
from src.users.application.user_service import UserService
from src.users.infrastructure.user_postgres__repo import UserPostgresRepository


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "repo_class, session",
    [
        (UserPostgresRepository, "postgres_async_session"),
    ],
    ids=[
        "Postgres repo",
    ],
)
async def test_can_get_all_users(repo_class, session, request) -> None:
    # given
    repo = repo_class(request.getfixturevalue(session))
    service = UserService(user_repo=repo)

    # when
    result = await service.get_all()

    # then
    assert len(result) >= 3


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
@pytest.mark.xfail(reason="some bug")
@pytest.mark.parametrize(
    "repo_class, session",
    [
        (UserPostgresRepository, "postgres_async_session"),
    ],
    ids=[
        "Postgres repo",
    ],
)
async def test_can_get_user_by_id(repo_class, session, request) -> None:
    # given
    repo = repo_class(request.getfixturevalue(session))
    service = UserService(user_repo=repo)
    # when

    result = await service.get_user_by_id(id=1)

    # then
    assert type(result) == UserDTO
    assert result.id == 1


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "repo_class, session",
    [
        (UserPostgresRepository, "postgres_async_session"),
    ],
    ids=[
        "Postgres repo",
    ],
)
async def test_can_create_user(repo_class, session, request) -> None:
    # given
    repo = repo_class(request.getfixturevalue(session))
    service = UserService(user_repo=repo)
    # создается без тэгов, логика их добавления в services
    data = {
        "username": "username",
        "password": "password",
    }

    new_user = CreateUserDTO(**data)
    # when
    result = await service.create_user(input_dto=new_user)
    print("add_one result", result)
    # then
    assert type(result) == UserDTO
    assert result.username == "username"


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "repo_class, session",
    [
        (UserPostgresRepository, "postgres_async_session"),
    ],
    ids=[
        "Postgres repo",
    ],
)
async def test_can_update_one_user(repo_class, session, request) -> None:
    # given
    repo = repo_class(request.getfixturevalue(session))
    service = UserService(user_repo=repo)
    data = {
        "username": "username_updated",
        "password": "password_updated",
    }

    user_update = UpdateUserDTO(**data)
    item = await service.get_all()
    # when
    result = await service.update_user(id=item[0].id, input_dto=user_update)

    # then
    assert type(result) == UserDTO
    assert result.username == "username_updated"


@pytest.mark.xfail(reason="some bug")
@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "repo_class, session",
    [
        (UserPostgresRepository, "postgres_async_session"),
    ],
    ids=[
        "Postgres repo",
    ],
)
async def test_can_delete_user(repo_class, session, request) -> None:
    # given
    repo = repo_class(request.getfixturevalue(session))
    service = UserService(user_repo=repo)
    item = await service.get_all()
    # when
    result = await service.delete_user(id=item[0].id)

    # then
    assert type(result) == int


@pytest.mark.usefixtures("seed_users_db")
@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "repo_class, session",
    [
        (UserPostgresRepository, "postgres_async_session"),
    ],
    ids=[
        "Postgres repo",
    ],
)
async def test_can_get_users_by_field(repo_class, session, request) -> None:
    # given
    repo = repo_class(request.getfixturevalue(session))
    service = UserService(user_repo=repo)

    # when
    result = await service.get_users_by_filter(
        params={
            "username": "username_updated",
            "password": "password_updated",
        }
    )

    # then
    assert type(result) == list
    assert len(result) >= 1
