from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict
import json
import os


class ServiceConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class TelegramSettings(ServiceConfig):
    token: str

    model_config = SettingsConfigDict(env_prefix="TELEGRAM_")

class DB(ServiceConfig):
    host: str = "localhost"
    port: int = 5432
    password: str
    user: str
    db: str

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    @property
    def root(self):
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@search_bot-database:{self.port}"
        )

    @property
    def uri(self):
        return f"{self.root}/{self.db}"
    
class Settings(ServiceConfig):
    telegram: TelegramSettings = TelegramSettings()
    db: DB = DB()

settings = Settings()
