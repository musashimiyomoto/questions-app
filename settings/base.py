from pathlib import Path

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

BASE_PATH = Path(__file__).parent.parent


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=f"{BASE_PATH}/.env",
        extra="ignore",
    )
