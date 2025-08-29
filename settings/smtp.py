from pydantic import Field
from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="smtp_")

    host: str = Field(default="mailcatcher", title="SMTP host")
    port: int = Field(default=1025, title="SMTP port")
    ssl: bool = Field(default=False, title="SMTP SSL")
    username: str = Field(default="noreply@example.com", title="SMTP username")
    password: str = Field(default="", title="SMTP password")


smtp_settings = SMTPSettings()
