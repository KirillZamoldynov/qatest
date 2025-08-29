"""API эндпоинты для работы с ответами"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.crud.answers import answer_crud
from app.schemas.schemas import AnswerResponse

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}", response_model=AnswerResponse)
async def get_answer(
    answer_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить конкретный ответ"""
    answer = await answer_crud.get_by_id(db, answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ответ с ID {answer_id} не найден"
        )
    return answer


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    answer_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить ответ"""
    answer = await answer_crud.get_by_id(db, answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ответ с ID {answer_id} не найден"
        )
    await answer_crud.delete(db, answer)