# # src/infrastructure/configuration/app_settings.py
# from pydantic import BaseSettings, PostgresDsn

# class AppSettings(BaseSettings):
#     DATABASE_URL: PostgresDsn
#     SECRET_KEY: str
#     JWT_ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#     ENCRYPTION_KEY: str
#     DEBUG: bool = False
    
#     class Config:
#         env_file = ".env"

# appSettings = AppSettings()



from pathlib import Path


ENV_PATH = Path(__file__).parent.parent.parent.parent / "config" / "environments" / "development.env"

# infrastructure/configuration/app_settings.py
import os
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings"""
    debug: bool = Field(default=False)
    environment: str = Field(default="development")

    # Database settings
    db_type: str = Field(default="postgresql")
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=6543)
    db_name: str = Field(default="tax_residency_db")
    db_user: str = Field(default="myuser")
    db_password: str = Field(default="mypassword")

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Global settings instance
settings = get_settings()




