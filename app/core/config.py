from enum import StrEnum
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = Path(__file__).resolve().parents[2] / ".env"


class Environment(StrEnum):
    DEVELOP = "develop"
    PRODUCTION = "production"


class Settings(BaseSettings):
    app_name: str = "Counsy"
    debug: bool = False
    environment: Environment = Environment.DEVELOP

    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )


settings = Settings()
