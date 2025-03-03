from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    LANGFLOW_API_URL: str = "http://localhost:7860"
    API_PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()