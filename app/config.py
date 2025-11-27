from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 
    DATABASE_URL: str = Field(...)

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
