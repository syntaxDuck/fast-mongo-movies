import pathlib

from pydantic_core.core_schema import StringSchema
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = pathlib.Path(__file__).parent / ".env"


class CommonSettings(BaseSettings):
    APP_NAME: str = "TODO"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    PROTOCOL: str
    DB_USER: str
    PASS: str
    HOST: str

    model_config = SettingsConfigDict(env_file=env_file)


class Settings(CommonSettings, ServerSettings):
    pass


settings = Settings()
