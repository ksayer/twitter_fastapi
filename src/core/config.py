import os
from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "some_project"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    TEST_POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None
    TEST_SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None
    API_PREFIX_V1: str
    MEDIA_ROOT: str = 'media/'
    MEDIA_URL: str
    DEBUG: bool = False

    @validator("MEDIA_ROOT", pre=True)
    def assemble_media_root(cls, value: str | None):
        src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_root = '/'.join([src_dir, value])  # type: ignore
        if not os.path.exists(media_root):
            os.mkdir(media_root)
        return media_root

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @validator("TEST_SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_test_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('TEST_POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = "../.env"


settings = Settings()  # type: ignore
