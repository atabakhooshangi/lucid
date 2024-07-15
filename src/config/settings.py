from pathlib import Path
from typing import Any, Optional
from pydantic import MySQLDsn, field_validator
from dotenv import load_dotenv
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

# Set up the base directory and load environment variables
BASE_DIR = Path(__file__).resolve().parents[0]
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """
    Settings class to hold the configuration for the MySQL database connection.
    The values are loaded from environment variables.
    """
    MYSQL_SERVER: str
    MYSQL_PORT: int
    MYSQL_DB: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_SCHEME: str = "mysql+asyncmy"  # Default scheme for async MySQL connections
    BACKEND_CORS_ORIGINS: bool = True
    SERVER_PORT: int
    RELOAD: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5040

    USER_RSA_PRIVATE_KEY: str
    USER_RSA_PUBLIC_KEY: str
    SERVER_HOST: str = "localhost"
    PAYLOAD_MAX_SIZE: int = 1  # Payload max size in MB
    DOMAIN: Optional[str] = None
    SQLALCHEMY_ASYNC_DATABASE_URI: Optional[MySQLDsn] = None
    CACHE_TIME: int = 300  # Cache time in seconds

    def get_async_connection_url(self) -> str:
        """
        Constructs the asynchronous connection URL for SQLAlchemy.

        Returns:
            str: The constructed async database connection URL.
        """
        return f"{self.MYSQL_SCHEME}://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    @field_validator("SQLALCHEMY_ASYNC_DATABASE_URI", mode="before")
    def assemble_async_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        """
        Assembles the async database connection URL if not provided directly.

        Args:
            v (Optional[str]): The provided database URL, if any.
            values (ValidationInfo): A dictionary of field values.

        Returns:
            Any: The assembled database connection URL.
        """
        if v:
            return v

        return MySQLDsn.build(
            scheme=values.data.get("MYSQL_SCHEME"),
            username=values.data.get("MYSQL_USER"),
            password=values.data.get("MYSQL_PASSWORD"),
            host=values.data.get("MYSQL_SERVER"),
            port=str(values.data.get("MYSQL_PORT")),
            path=f"/{values.data.get('MYSQL_DB') or ''}",
        )


# Instantiate the settings object to load the configuration
settings: Settings = Settings()
settings.DOMAIN = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
