from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = Path(__file__).resolve().parent / ".env"


class DBSettings(BaseModel):
    url: str = Field(
        default="postgresql+asyncpg://counsy:counsy@db:5432/con",
        description="DSN для соединения с PostgreSQL",
    )
    pool_size: int = Field(default=10, description="Размер пула соединений")
    max_overflow: int = Field(
        default=20,
        description="Максимальное количество дополнительных временных соединений с базой данных сверх лимита",
    )
    pool_timeout: int = Field(
        default=30,
        description="Время ожидания соединения",
    )
    pool_recycle: int = Field(
        default=300,
        description="Время в секундах, по истечении которого соединение с базой данных будет принудительно пересоздано",
    )
    pool_pre_ping: bool = Field(
        default=True,
        description="Проверка соединения перед каждым использованием",
    )


class Environment(StrEnum):
    DEVELOP = "develop"
    PRODUCTION = "production"


class Settings(BaseSettings):
    app_name: str = "Counsy"
    debug: bool = False
    environment: Environment = Environment.DEVELOP
    db: DBSettings = DBSettings()

    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )


settings = Settings()
