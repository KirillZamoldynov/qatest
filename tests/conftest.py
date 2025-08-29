"""Конфигурация для тестов."""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_async_session
from app.main import app

# URL тестовой базы данных
TEST_DATABASE_URL = "postgresql+asyncpg://QAdmin:QPassword@localhost:5432/test_qatest"

# Создание тестового движка
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True
)

# Фабрика тестовых сессий
TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Создание event loop для тестов."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Создание тестовой сессии базы данных."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Создание тестового клиента."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()