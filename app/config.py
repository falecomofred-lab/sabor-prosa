from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./sabor_prosa.db"
    JWT_SECRET_KEY: str = "sabor-e-prosa-2026-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440
    ANTHROPIC_API_KEY: str = ""
    AI_MODEL: str = "claude-sonnet-4-5-20250929"
    GOOGLE_MAPS_API_KEY: str = ""
    APP_NAME: str = "Sabor e Prosa Empório API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
@lru_cache()
def get_settings() -> Settings:
    return Settings()
