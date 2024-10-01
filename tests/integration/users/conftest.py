import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.infrastructure.models.user_model import UserModel


@pytest.fixture(scope="module")
@pytest.mark.asyncio(scope="module")
async def seed_users_db(postgres_async_session: AsyncSession) -> None:
    user_data = [
        {
            "id": 1,
            "username": "user1",
            "password": "password1",
        },
        {
            "id": 2,
            "username": "user2",
            "password": "password2",
        },
        {
            "id": 3,
            "username": "user3",
            "password": "password3",
        },
    ]
    async with postgres_async_session() as session:
        id_tuple = tuple(note["id"] for note in user_data)
        exist_data = await session.execute(select(UserModel).filter(UserModel.id.in_(id_tuple)))
        result_id_list = []
        result_id_list = [note.id for note in exist_data.scalars().all()]
        print("result_id_list ", result_id_list)
        for note in user_data:
            if note["id"] not in result_id_list:
                print("add new", note["id"])

                session.add(UserModel(**note))
        await session.commit()
