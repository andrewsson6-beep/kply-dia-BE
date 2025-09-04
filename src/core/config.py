import os
from typing import ClassVar, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from core.path_config import ROOT_PATH

class Settings(BaseSettings):
    PROJECT_NAME: str = "kply_dialysis"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server settings (updated to 8080)
    # HOST: str = "127.0.0.1"  # Default to localhost for security
    # PORT: int = 8000         # <-- Changed to 8080

    # Time settings
    DATETIME_TIMEZONE: str = "Asia/Kolkata"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    
    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=f"{ROOT_PATH}\.env",  # Load .env file
        env_file_encoding="utf-8",
        case_sensitive=False,  # Allow lowercase env vars (e.g., "port=8080")
        extra="ignore"
    )


    GOOGLE_CLIENT_ID: str 
    GOOGLE_CLIENT_SECRET: str

    DATABASE_TYPE:str
   

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    FASTAPI_API_V1_PATH: str = '/api/v1'

    DATABASE_SCHEMA: str
    DATABASE_CHARSET:str

    DATABASE_ECHO: bool = False
    DATABASE_POOL_ECHO: bool = False
  
    # Token
    TOKEN_ALGORITHM: str
    TOKEN_SECRET_KEY: str
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24  
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7

    CORS_EXPOSE_HEADERS: list[str] = [
        'X-Request-ID',
    ]
    CORS_ALLOWED_ORIGINS: list[str] = [ 
        "http://localhost:4200",
    ]


    


settings = Settings()