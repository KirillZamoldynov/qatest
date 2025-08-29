"""Основное приложение FastAPI"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api import health
from app.api.routers import answers, questions
from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    general_exception_handler,
)
from app.core.logging import log_request_middleware, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Управление жизненным циклом приложения.

    Args:
        app: Экземпляр FastAPI приложения

    Yields:
        None
    """
    # Настройка при запуске
    setup_logging()
    logger.info(f"Запуск {settings.app_title} v{settings.app_version}")
    logger.info(f"Документация доступна на /docs")
    logger.info(f"Debug mode: {settings.debug}")

    yield

    # Очистка при остановке
    logger.info("Остановка приложения..")


# Создание приложения
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Обработчики исключений
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Настройка CORS (в prod нужно будет изменить подход)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для логирования
@app.middleware("http")
async def add_logging_middleware(request, call_next):
    """Добавить middleware для логирования запросов"""
    return await log_request_middleware(request, call_next)

# Подключение роутеров
app.include_router(health.router)
app.include_router(questions.router)
app.include_router(answers.router)


@app.get("/", tags=["root"])
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Q&A Service API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }