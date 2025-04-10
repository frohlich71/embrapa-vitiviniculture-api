from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Load environment variables and configuration settings.
    """
    DATABASE_URL: str = "sqlite:///./local.db"
    ALLOW_REINGEST: bool = False

    class Config:
        env_file = ".env"


settings = Settings()