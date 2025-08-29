"""Конфигурация приложения"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения"""

    # Настройки базы данных
    postgres_user: str = "QAdmin"
    postgres_password: str = "QPassword"
    postgres_db: str = "QAtest"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Настройки приложения
    app_title: str = "Q&A Service API"
    app_version: str = "1.0"
    debug: bool = False

    @property
    def database_url(self) -> str:
        """Получить URL для подключения к базе данных"""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()


def get_settings() -> Settings:
    """Получить экземпляр настроек приложения"""
    return settings