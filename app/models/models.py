"""Модели для вопросов и ответов"""

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Question(Base):
    """Модель вопроса"""

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # Связь с ответами
    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        """Строковое представление объекта"""
        return f"<Question(id={self.id}, text={self.text[:50]}...)>"


class Answer(Base):
    """Модель ответа на вопрос"""

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[str] = mapped_column(String(100), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # Связь с вопросом
    question: Mapped["Question"] = relationship(
        back_populates="answers",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        """Строковое представление объекта"""
        return f"<Answer(id={self.id}, question_id={self.question_id}, user_id={self.user_id})>"