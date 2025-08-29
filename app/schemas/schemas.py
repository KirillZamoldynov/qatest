"""Pydantic схемы для валидации данных"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AnswerBase(BaseModel):
    """Базовая схема ответа"""

    user_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Идентификатор пользователя"
    )
    text: str = Field(
        ...,
        min_length=1,
        description="Текст ответа"
    )

    @classmethod
    @field_validator("text", "user_id")
    def validate_not_empty(cls, v: str, field) -> str:
        """Валидация на пустые строки"""
        v = v.strip()
        if not v:
            raise ValueError(f"{field.field_name} не может быть пустым")
        return v


class AnswerCreate(AnswerBase):
    """Схема для создания ответа"""
    pass


class AnswerResponse(AnswerBase):
    """Схема для ответа API"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    created_at: datetime
    updated_at: datetime


class QuestionBase(BaseModel):
    """Базовая схема вопроса"""

    text: str = Field(
        ...,
        min_length=1,
        description="Текст вопроса"
    )

    @classmethod
    @field_validator("text")
    def validate_text(cls, v: str) -> str:
        """Валидация текста вопроса"""
        v = v.strip()
        if not v:
            raise ValueError("Текст вопроса не может быть пустым")
        if len(v) < 3:
            raise ValueError("Текст вопроса должен содержать минимум 3 символа")
        return v


class QuestionCreate(QuestionBase):
    """Схема для создания вопроса"""
    pass


class QuestionResponse(QuestionBase):
    """Схема для ответа API без ответов"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class QuestionWithAnswers(QuestionResponse):
    """Схема вопроса с ответами"""

    answers: List[AnswerResponse] = Field(
        default_factory=list,
        description="Список ответов на вопрос"
    )


class PaginationParams(BaseModel):
    """Параметры пагинации"""

    page: int = Field(1, ge=1, description="Номер страницы")
    page_size: int = Field(10, ge=1, le=100, description="Размер страницы")


class PaginatedResponse(BaseModel):
    """Ответ с пагинацией"""

    items: List[QuestionResponse]
    total: int
    page: int
    page_size: int
    pages: int