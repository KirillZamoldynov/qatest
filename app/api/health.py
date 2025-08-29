"""Health check и статус эндпоинты"""

from fastapi import APIRouter, Depends, status
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_session

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Проверка здоровья сервиса"
)
async def health_check():
    """Базовая проверка здоровья сервиса.

    Returns:
        Статус сервиса
    """
    return {
        "status": "healthy",
        "service": settings.app_title,
        "version": settings.app_version
    }


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Проверка готовности сервиса"
)
async def readiness_check(
    db: AsyncSession = Depends(get_async_session)
):
    """Проверка готовности сервиса к работе.

    Проверяет доступность базы данных.

    Args:
        db: Сессия базы данных

    Returns:
        Статус готовности
    """
    try:
        # Проверяем соединение с БД
        result = await db.execute(text("SELECT 1"))
        result.scalar()

        logger.debug("Database connection check: OK")

        return {
            "status": "ready",
            "database": "connected",
            "service": settings.app_title
        }
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return {
            "status": "not ready",
            "database": "disconnected",
            "error": str(e)
        }


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Проверка жизнеспособности"
)
async def liveness_check():
    """Проверка жизнеспособности сервиса.

    Returns:
        Статус жизнеспособности
    """
    return {"status": "alive"}


@router.get(
    "/metrics",
    status_code=status.HTTP_200_OK,
    summary="Метрики сервиса"
)
async def metrics(
    db: AsyncSession = Depends(get_async_session)
):
    """Получить метрики сервиса.

    Args:
        db: Сессия базы данных

    Returns:
        Метрики сервиса
    """
    try:
        # Подсчет вопросов
        questions_count = await db.execute(
            text("SELECT COUNT(*) FROM questions")
        )
        questions_total = questions_count.scalar()

        # Подсчет ответов
        answers_count = await db.execute(
            text("SELECT COUNT(*) FROM answers")
        )
        answers_total = answers_count.scalar()

        # Подсчет уникальных пользователей
        users_count = await db.execute(
            text("SELECT COUNT(DISTINCT user_id) FROM answers")
        )
        users_total = users_count.scalar()

        logger.debug(
            f"Metrics: questions={questions_total}, "
            f"answers={answers_total}, users={users_total}"
        )

        return {
            "questions_total": questions_total,
            "answers_total": answers_total,
            "unique_users": users_total,
            "avg_answers_per_question": (
                round(answers_total / questions_total, 2)
                if questions_total > 0 else 0
            )
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return {
            "error": "Unable to fetch metrics",
            "details": str(e)
        }