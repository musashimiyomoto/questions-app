from pydantic import Field
from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="auth_")

    secret_key: str = Field(default="secret", title="Secret key")
    algorithm: str = Field(default="HS256", title="Algorithm")
    access_token_expire_minutes: int = Field(
        default=30, title="Access token expire minutes"
    )
    token_type: str = Field(default="Bearer", title="Token type")
    verify_code_ttl: int = Field(default=60, title="Verify email code ttl")


auth_settings = AuthSettings()
