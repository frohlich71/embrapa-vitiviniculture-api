import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """
    Load environment variables and configuration settings.
    """

    DATABASE_URL: str
    ALLOW_REINGEST: bool = False

    # JWT settings
    JWT_SECRET_KEY: str = "f35b5633979ab1d65ef3c3e770455d30bd903dccd5dd6fcb305fe33a9f49fd19"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()
