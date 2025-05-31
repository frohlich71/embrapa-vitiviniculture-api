import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Load environment variables and configuration settings.
    """

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ALLOW_REINGEST: bool = os.getenv("ALLOW_REINGEST", "false").lower() == "true"
    EMBRAPA_BASE_URL: str = os.getenv(
        "EMBRAPA_BASE_URL", "http://vitibrasil.cnpuv.embrapa.br"
    )

    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # Default admin user
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@embrapa.br")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")

    class Config:
        env_file = ".env"


settings = Settings()
