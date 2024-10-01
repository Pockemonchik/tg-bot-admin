import os
from datetime import datetime, timezone

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from src.di import Container
from src.users.application.user_service import UserService


def get_token(request: Request):
    token = request.headers.get("token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token


@inject
async def get_current_user(
    token: str = Depends(get_token), user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        auth_data = {
            "secret_key": os.environ.get(
                "SECRET_KEY",
                "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt",
            ),
            "algorithm": os.environ.get(
                "ALGORITHM",
                "HS256",
            ),
        }
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный!")

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя")

    user = await user_service.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
