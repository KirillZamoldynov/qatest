"""Тесты для API эндпоинтов."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_question(client: AsyncClient):
    """Тест создания вопроса"""
    response = await client.post(
        "/questions/",
        json={"text": "Какой язык программирования лучше?"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Какой язык программирования лучше?"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_all_questions(client: AsyncClient):
    """Тест получения всех вопросов"""
    # Создаем несколько вопросов
    await client.post("/questions/", json={"text": "Вопрос 1"})
    await client.post("/questions/", json={"text": "Вопрос 2"})

    response = await client.get("/questions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_question_with_answers(client: AsyncClient):
    """Тест получения вопроса с ответами"""
    # Создаем вопрос
    question_response = await client.post(
        "/questions/",
        json={"text": "Тестовый вопрос"}
    )
    question_id = question_response.json()["id"]

    # Добавляем ответы
    await client.post(
        f"/questions/{question_id}/answers/",
        json={"user_id": "user1", "text": "Ответ 1"}
    )
    await client.post(
        f"/questions/{question_id}/answers/",
        json={"user_id": "user2", "text": "Ответ 2"}
    )

    # Получаем вопрос с ответами
    response = await client.get(f"/questions/{question_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Тестовый вопрос"
    assert len(data["answers"]) == 2


@pytest.mark.asyncio
async def test_create_answer_for_nonexistent_question(client: AsyncClient):
    """Тест создания ответа для несуществующего вопроса"""
    response = await client.post(
        "/questions/999/answers/",
        json={"user_id": "user1", "text": "Ответ"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_question_with_answers(client: AsyncClient):
    """Тест удаления вопроса с ответами"""
    # Создаем вопрос
    question_response = await client.post(
        "/questions/",
        json={"text": "Вопрос для удаления"}
    )
    question_id = question_response.json()["id"]

    # Добавляем ответ
    await client.post(
        f"/questions/{question_id}/answers/",
        json={"user_id": "user1", "text": "Ответ"}
    )

    # Удаляем вопрос
    response = await client.delete(f"/questions/{question_id}")
    assert response.status_code == 204

    # Проверяем, что вопрос удален
    response = await client.get(f"/questions/{question_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_answer(client: AsyncClient):
    """Тест удаления ответа"""
    # Создаем вопрос
    question_response = await client.post(
        "/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["id"]

    # Создаем ответ
    answer_response = await client.post(
        f"/questions/{question_id}/answers/",
        json={"user_id": "user1", "text": "Ответ для удаления"}
    )
    answer_id = answer_response.json()["id"]

    # Удаляем ответ
    response = await client.delete(f"/answers/{answer_id}")
    assert response.status_code == 204

    # Проверяем, что ответ удален
    response = await client.get(f"/answers/{answer_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_validation_empty_text(client: AsyncClient):
    """Тест валидации пустого текста"""
    response = await client.post(
        "/questions/",
        json={"text": "   "}
    )
    assert response.status_code == 422

    # Создаем вопрос для теста ответа
    question_response = await client.post(
        "/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["id"]

    response = await client.post(
        f"/questions/{question_id}/answers/",
        json={"user_id": "user1", "text": "   "}
    )
    assert response.status_code == 422