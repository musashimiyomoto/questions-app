import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models.base import Base
from app.db.session import get_db
from app.core.config import settings

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/test_questions_db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def sample_question(async_client: AsyncClient):
    response = await async_client.post(
        "/questions/",
        json={"text": "What is FastAPI?"}
    )
    return response.json()


class TestQuestions:
    async def test_create_question(self, async_client: AsyncClient):
        response = await async_client.post(
            "/questions/",
            json={"text": "What is Python?"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["text"] == "What is Python?"
        assert "id" in data
        assert "created_at" in data

    async def test_create_question_empty_text(self, async_client: AsyncClient):
        response = await async_client.post(
            "/questions/",
            json={"text": ""}
        )
        assert response.status_code == 422

    async def test_get_questions(self, async_client: AsyncClient, sample_question):
        response = await async_client.get("/questions/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    async def test_get_question_by_id(self, async_client: AsyncClient, sample_question):
        question_id = sample_question["id"]
        response = await async_client.get(f"/questions/{question_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == question_id
        assert data["text"] == "What is FastAPI?"

    async def test_get_question_not_found(self, async_client: AsyncClient):
        response = await async_client.get("/questions/99999")
        assert response.status_code == 404

    async def test_delete_question(self, async_client: AsyncClient, sample_question):
        question_id = sample_question["id"]
        response = await async_client.delete(f"/questions/{question_id}")
        assert response.status_code == 204

        response = await async_client.get(f"/questions/{question_id}")
        assert response.status_code == 404

    async def test_delete_question_not_found(self, async_client: AsyncClient):
        response = await async_client.delete("/questions/99999")
        assert response.status_code == 404


class TestAnswers:
    async def test_create_answer(self, async_client: AsyncClient, sample_question):
        question_id = sample_question["id"]
        response = await async_client.post(
            f"/questions/{question_id}/answers/",
            json={"user_id": "user123", "text": "FastAPI is a web framework"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == "user123"
        assert data["text"] == "FastAPI is a web framework"
        assert data["question_id"] == question_id

    async def test_create_answer_invalid_question(self, async_client: AsyncClient):
        response = await async_client.post(
            "/questions/99999/answers/",
            json={"user_id": "user123", "text": "Some answer"}
        )
        assert response.status_code == 404

    async def test_create_answer_empty_text(self, async_client: AsyncClient, sample_question):
        question_id = sample_question["id"]
        response = await async_client.post(
            f"/questions/{question_id}/answers/",
            json={"user_id": "user123", "text": ""}
        )
        assert response.status_code == 422

    async def test_get_answer(self, async_client: AsyncClient, sample_question):
        question_id = sample_question["id"]
        
        create_response = await async_client.post(
            f"/questions/{question_id}/answers/",
            json={"user_id": "user456", "text": "Great question!"}
        )
        answer_id = create_response.json()["id"]

        response = await async_client.get(f"/answers/{answer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == answer_id
        assert data["user_id"] == "user456"
        assert data["text"] == "Great question!"

    async def test_get_answer_not_found(self, async_client: AsyncClient):
        response = await async_client.get("/answers/99999")
        assert response.status_code == 404

    async def test_delete_answer(self, async_client: AsyncClient, sample_question):
        question_id = sample_question["id"]
        
        create_response = await async_client.post(
            f"/questions/{question_id}/answers/",
            json={"user_id": "user789", "text": "Answer to delete"}
        )
        answer_id = create_response.json()["id"]

        response = await async_client.delete(f"/answers/{answer_id}")
        assert response.status_code == 204

        response = await async_client.get(f"/answers/{answer_id}")
        assert response.status_code == 404

    async def test_delete_answer_not_found(self, async_client: AsyncClient):
        response = await async_client.delete("/answers/99999")
        assert response.status_code == 404

    async def test_cascade_delete_answers_with_question(self, async_client: AsyncClient, sample_question):
        question_id = sample_question["id"]
        
        answer_response = await async_client.post(
            f"/questions/{question_id}/answers/",
            json={"user_id": "user999", "text": "This should be deleted too"}
        )
        answer_id = answer_response.json()["id"]

        await async_client.delete(f"/questions/{question_id}")

        response = await async_client.get(f"/answers/{answer_id}")
        assert response.status_code == 404


class TestHealthCheck:
    async def test_root_endpoint(self, async_client: AsyncClient):
        response = await async_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Questions & Answers API"}

    async def test_health_check(self, async_client: AsyncClient):
        response = await async_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
