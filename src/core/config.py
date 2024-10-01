import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    mode: str = os.environ.get("MODE", "DEV")

    postgres_url: str = os.environ.get("DB_URL", "locahost")
    postgres_echo: bool = bool(os.environ.get("DB_ECHO", False))


def get_settings():
    return Settings()
