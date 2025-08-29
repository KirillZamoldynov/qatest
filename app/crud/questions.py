"""CRUD операции для вопросов"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import Question
from app.schemas.schemas import QuestionCreate


class QuestionCRUD:
    """CRUD операции для работы с вопросами"""

    @staticmethod
    async def create(
            db: AsyncSession,
            question_data: QuestionCreate
    ) -> Question:
        """Создать новый вопрос"""
        question = Question(**question_data.model_dump())
        db.add(question)
        await db.commit()
        await db.refresh(question)
        return question

    @staticmethod
    async def get_all(db: AsyncSession) -> List[Question]:
        """Получить все вопросы"""
        result = await db.execute(
            select(Question).order_by(Question.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(
            db: AsyncSession,
            question_id: int
    ) -> Optional[Question]:
        """Получить вопрос по ID"""
        result = await db.execute(
            select(Question).where(Question.id == question_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_with_answers(
            db: AsyncSession,
            question_id: int
    ) -> Optional[Question]:
        """Получить вопрос с ответами"""
        result = await db.execute(
            select(Question)
            .options(selectinload(Question.answers))
            .where(Question.id == question_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
            db: AsyncSession,
            question: Question
    ) -> None:
        """Удалить вопрос"""
        await db.delete(question)
        await db.commit()


question_crud = QuestionCRUD()