import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    NETWORK: str

    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()  # type: ignore


def get_db_url() -> str:
    if os.environ.get("POSTGRES_HOST"):
        return (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
                f"{os.environ.get('POSTGRES_HOST')}:{settings.DB_PORT}/{settings.POSTGRES_DB}")
    return (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.POSTGRES_DB}")


database_url = get_db_url()
