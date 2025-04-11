import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Load environment variables and configuration settings.
    """

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./local.db")
    ALLOW_REINGEST: bool = os.getenv("ALLOW_REINGEST", "false").lower() == "true"

    class Config:
        env_file = ".env"


settings = Settings()
