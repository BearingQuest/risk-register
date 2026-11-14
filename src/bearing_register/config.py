"""Settings, read from BRG_* environment variables. The only module that reads the environment."""

from typing import Literal

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from bearing_register.errors import ConfigError

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BRG_", extra="ignore", frozen=True)

    log_level: LogLevel = "INFO"


def load_settings() -> Settings:
    """Read the settings, or raise ConfigError naming the bad fields (never their values)."""
    try:
        return Settings()
    except ValidationError as error:
        fields = sorted({".".join(str(part) for part in e["loc"]) for e in error.errors()})
        raise ConfigError(f"invalid configuration: {', '.join(fields)}") from None
