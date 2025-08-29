"""Обработка исключений приложения"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger


class AppException(Exception):
    """Базовое исключение приложения"""

    def __init__(self, message: str, status_code: int = 500):
        """Инициализация исключения.

        Args:
            message: Сообщение об ошибке
            status_code: HTTP статус код
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Исключение для несуществующих ресурсов."""

    def __init__(self, message: str = "Ресурс не найден"):
        """Инициализация исключения"""
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ValidationError(AppException):
    """Исключение для ошибок валидации"""

    def __init__(self, message: str = "Ошибка валидации данных"):
        """Инициализация исключения"""
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


class DatabaseError(AppException):
    """Исключение для ошибок базы данных"""

    def __init__(self, message: str = "Ошибка базы данных"):
        """Инициализация исключения"""
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


async def app_exception_handler(request: Request, exc: AppException):
    """Обработчик исключений приложения.

    Args:
        request: HTTP запрос
        exc: Исключение приложения

    Returns:
        JSON ответ с ошибкой
    """
    logger.warning(
        f"Application exception: {exc.message} | "
        f"Status: {exc.status_code} | "
        f"Path: {request.url.path}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Обработчик общих исключений.

    Args:
        request: HTTP запрос
        exc: Исключение

    Returns:
        JSON ответ с ошибкой
    """
    logger.exception(
        f"Unhandled exception on {request.url.path}: {str(exc)}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Внутренняя ошибка сервера",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "path": str(request.url.path)
        }
    )


async def validation_exception_handler(request: Request, exc: HTTPException):
    """Обработчик исключений валидации.

    Args:
        request: HTTP запрос
        exc: HTTP исключение

    Returns:
        JSON ответ с ошибкой
    """
    logger.warning(
        f"Validation error on {request.url.path}: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        }
    )