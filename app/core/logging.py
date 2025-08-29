"""Настройка логирования приложения"""

import sys
from typing import Any

from loguru import logger
from starlette.requests import Request

from app.core.config import settings


def setup_logging() -> None:
    """Настроить логирование для приложения"""

    # Формат для консоли
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Добавляем консольный вывод
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.debug else "INFO",
        colorize=True,
        backtrace=settings.debug,
        diagnose=settings.debug
    )

    # Добавляем файловый вывод
    if not settings.debug:
        logger.add(
            "logs/app_{time:YYYY-MM-DD}.log",
            rotation="00:00",  # Новый файл каждый день
            retention="30 days",  # Хранить логи 30 дней
            compression="zip",  # Сжимать старые логи
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            backtrace=True,
            diagnose=False
        )

        # Отдельный файл для ошибок
        logger.add(
            "logs/errors_{time:YYYY-MM-DD}.log",
            rotation="00:00",
            retention="60 days",
            compression="zip",
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
            backtrace=True,
            diagnose=True
        )

    logger.info(f"Логирование настроено. Debug mode: {settings.debug}")


async def log_request_middleware(request: Request, call_next: Any) -> Any:
    """Middleware для логирования HTTP запросов.

    Args:
        request: HTTP запрос
        call_next: Следующий обработчик

    Returns:
        HTTP ответ
    """
    # Получаем IP клиента
    client_ip = request.client.host if request.client else "unknown"

    # Логируем входящий запрос
    logger.info(
        f"{request.method} {request.url.path} | "
        f"Client: {client_ip}"
    )

    # Обрабатываем запрос
    try:
        response = await call_next(request)

        # Логируем успешный ответ
        logger.info(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code}"
        )

        return response
    except Exception as e:
        # Логируем ошибку
        logger.error(
            f"{request.method} {request.url.path} | "
            f"Error: {str(e)}"
        )
        raise