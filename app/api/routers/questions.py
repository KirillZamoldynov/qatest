"""API эндпоинты для работы с вопросами"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.crud.answers import answer_crud
from app.crud.questions import question_crud
from app.schemas.schemas import (
    AnswerCreate,
    AnswerResponse,
    QuestionCreate,
    QuestionResponse,
    QuestionWithAnswers,
)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[QuestionResponse])
async def get_all_questions(
        db: AsyncSession = Depends(get_async_session)
):
    """Получить список всех вопросов"""
    questions = await question_crud.get_all(db)
    return questions


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
        question_data: QuestionCreate,
        db: AsyncSession = Depends(get_async_session)
):
    """Создать новый вопрос"""
    question = await question_crud.create(db, question_data)
    return question


@router.get("/{question_id}", response_model=QuestionWithAnswers)
async def get_question_with_answers(
        question_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    """Получить вопрос и все ответы на него"""
    question = await question_crud.get_with_answers(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с ID {question_id} не найден"
        )
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
        question_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    """Удалить вопрос вместе со всеми ответами"""
    question = await question_crud.get_by_id(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с ID {question_id} не найден"
        )
    await question_crud.delete(db, question)


@router.post("/{question_id}/answers/", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
async def create_answer(
        question_id: int,
        answer_data: AnswerCreate,
        db: AsyncSession = Depends(get_async_session)
):
    """Добавить ответ к вопросу"""
    # Проверяем существование вопроса
    question = await question_crud.get_by_id(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вопрос с ID {question_id} не найден"
        )

    answer = await answer_crud.create(db, answer_data, question_id)
    return answer