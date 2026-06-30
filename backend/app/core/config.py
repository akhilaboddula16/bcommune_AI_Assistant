from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bcommune AI Assistant"
    app_env: str = "development"

    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    frontend_url: str = "http://localhost:5173"

    supabase_db_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    ai_engine_url: str
    bcom_internal_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()