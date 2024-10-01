from datetime import datetime
from unittest import mock

import pytest

from src.users.application.user_service import UserService
from src.users.domain.user_entity import User
from src.users.domain.user_repo import IUserRepository


@pytest.mark.asyncio(scope="module")
async def test_can_get_all_users() -> None:
    # given
    repo_mock = mock.AsyncMock(spec=IUserRepository)
    repo_mock.get_all.return_value = [
        User(
            id=1,
            owner_id=1,
            header="header",
            content="content",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    ]
    service = UserService(user_repo=repo_mock)

    # when
    result = await service.get_all()

    # then
    assert len(result) == 1
