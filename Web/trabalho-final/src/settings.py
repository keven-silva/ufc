import enum
import os
import secrets
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = bool(os.getenv("RELOAD", False))

    # Secret key for JWT
    secret_key: str = secrets.token_urlsafe(32)
    token_ttl: int = 24 * 60 * 60  # 24 hours
    jwt_algorithm: str = "HS256"

    # Application version
    version: str = os.getenv("VERSION", "1.0.0")
    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Path to the templates directory
    templates_dir: Path = Path(__file__).resolve().parent / "templates"
    # Path to the static directory
    static_dir: Path = Path(__file__).resolve().parent / "static"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
