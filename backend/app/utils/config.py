from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str

    JWT_SECRET: str

    JWT_REFRESH_SECRET: str

    OLLAMA_URL: str

    LLM_MODEL: str

    EMBED_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()