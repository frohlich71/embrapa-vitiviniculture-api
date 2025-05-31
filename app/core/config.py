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
    EMBRAPA_BASE_URL: str = os.getenv("EMBRAPA_BASE_URL", "http://vitibrasil.cnpuv.embrapa.br")

    class Config:
        env_file = ".env"


settings = Settings()
