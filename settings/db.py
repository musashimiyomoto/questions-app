from pydantic import Field
from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_")

    host: str = Field(default="localhost", title="Database host")
    port: int = Field(default=5432, title="Database port")
    login: str = Field(default="postgres", title="Database login")
    password: str = Field(default="postgres", title="Database password")
    name: str = Field(default="auth", title="Database name")

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.login}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.name}"
        )


db_settings = DbSettings()
