"""CRUD операции для ответов"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Answer
from app.schemas.schemas import AnswerCreate


class AnswerCRUD:
    """CRUD операции для работы с ответами"""

    @staticmethod
    async def create(
            db: AsyncSession,
            answer_data: AnswerCreate,
            question_id: int
    ) -> Answer:
        """Создать новый ответ на вопрос"""
        answer = Answer(
            **answer_data.model_dump(),
            question_id=question_id
        )
        db.add(answer)
        await db.commit()
        await db.refresh(answer)
        return answer

    @staticmethod
    async def get_by_id(
            db: AsyncSession,
            answer_id: int
    ) -> Optional[Answer]:
        """Получить ответ по ID"""
        result = await db.execute(
            select(Answer).where(Answer.id == answer_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
            db: AsyncSession,
            answer: Answer
    ) -> None:
        """Удалить ответ"""
        await db.delete(answer)
        await db.commit()


answer_crud = AnswerCRUD()