"""Настройка базы данных и базовые модели"""

from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    sessionmaker,
)

from app.core.config import settings

# Создание асинхронного движка
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Фабрика сессий
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Аннотации для типов
created_at = Annotated[
    datetime,
    mapped_column(
        server_default=func.now(),
        nullable=False
    )
]

updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
]


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех моделей"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Автоматическое создание имени таблицы"""
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


async def get_async_session() -> AsyncSession:
    """Получить асинхронную сессию базы данных"""
    async with async_session_maker() as session:
        yield session