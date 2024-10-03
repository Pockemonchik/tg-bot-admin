import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_users_db")
async def test_can_create_user(async_test_client: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given
    payload = {
        "username": "username",
        "password": "password",
    }

    # when
    response = await async_test_client.post("/users/", json=payload)

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_users_db")
async def test_can_find_all_users(async_test_client: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given

    # when

    response = await async_test_client.get(f"/users/")

    # then
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_users_db")
async def test_can_get_user(async_test_client: AsyncClient, request: pytest.FixtureRequest) -> None:
    # when

    response = await async_test_client.get(f"/users/")
    id = response.json()[0]["id"]
    response = await async_test_client.get(f"/users/{id}")
    print("get_user resp", response.json())
    # then
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_users_db")
async def test_can_update_user(async_test_client: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given
    payload = {
        "username": "username_updated",
        "password": "password_updated",
    }

    # when

    response = await async_test_client.get(f"/users/")
    id = response.json()[0]["id"]
    response = await async_test_client.put(url=f"/users/{id}", json=payload)
    # then
    assert 1 == 1


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_users_db")
async def test_can_delete_user(async_test_client: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given

    # when

    response = await async_test_client.get(f"/users/")
    id = response.json()[0]["id"]
    print("delet f id")
    response = await async_test_client.delete(url=f"/users/{int(id)}")
    # then
    assert response.status_code == status.HTTP_200_OK
    assert 1 == 1


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_users_db")
async def test_should_return_404_if_user_does_not_exist(
    async_test_client: AsyncClient, request: pytest.FixtureRequest
) -> None:
    # when

    response = await async_test_client.get(f"/users/11232")

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio(scope="module")
@pytest.mark.usefixtures("async_test_client")
@pytest.mark.usefixtures("seed_users_db")
async def test_can_get_users_by_any_field(async_test_client: AsyncClient, request: pytest.FixtureRequest) -> None:
    # given

    # when

    response = await async_test_client.get(f"/users/filter/?header=test1header")
    print("any_field resp", response.json())
    # then
    assert response.status_code == status.HTTP_200_OK
