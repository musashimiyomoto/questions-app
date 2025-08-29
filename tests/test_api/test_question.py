import pytest

from tests.factories import QuestionFactory
from tests.test_api.base import BaseTestCase


class TestGetAllQuestions(BaseTestCase):
    url = "/questions/"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        question1 = await QuestionFactory.create_async(
            session=self.session, text="What is Python?"
        )
        question2 = await QuestionFactory.create_async(
            session=self.session, text="How to use FastAPI?"
        )

        response = await self.client.get(url=self.url)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == question1.id
        assert data[0]["text"] == question1.text
        assert data[1]["id"] == question2.id
        assert data[1]["text"] == question2.text


class TestCreateQuestion(BaseTestCase):
    url = "/questions/"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        question_data = {"text": "What is the meaning of life?"}

        response = await self.client.post(url=self.url, json=question_data)

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["text"] == question_data["text"]
        assert "created_at" in data


class TestGetQuestionWithAnswers(BaseTestCase):
    url = "/questions/{id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        question = await QuestionFactory.create_async(
            session=self.session, text="What is Python?"
        )

        response = await self.client.get(url=self.url.format(id=question.id))

        data = await self.assert_response_ok(response=response)
        assert data["id"] == question.id
        assert data["text"] == question.text
        assert "answers" in data
        assert isinstance(data["answers"], list)
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_not_found(self) -> None:
        non_existent_id = 999999

        response = await self.client.get(url=self.url.format(id=non_existent_id))

        data = await self.assert_response_not_found(response=response)
        assert data["detail"] == "Question not found"


class TestDeleteQuestion(BaseTestCase):
    url = "/questions/{id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        question = await QuestionFactory.create_async(
            session=self.session, text="What is Python?"
        )

        response = await self.client.delete(url=self.url.format(id=question.id))

        await self.assert_response_no_content(response=response)

    @pytest.mark.asyncio
    async def test_not_found(self) -> None:
        non_existent_id = 999999

        response = await self.client.delete(url=self.url.format(id=non_existent_id))

        data = await self.assert_response_not_found(response=response)
        assert data["detail"] == "Question not found"
