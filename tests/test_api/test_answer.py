import uuid

import pytest

from tests.factories import AnswerFactory, QuestionFactory
from tests.test_api.base import BaseTestCase


class TestCreateAnswer(BaseTestCase):
    url = "/questions/{id}/answers/"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        question = await QuestionFactory.create_async(
            session=self.session, text="What is Python?"
        )
        user_id = uuid.uuid4()
        answer_data = {
            "user_id": str(user_id),
            "text": "Python is a programming language",
        }

        response = await self.client.post(
            url=self.url.format(id=question.id), json=answer_data
        )

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["user_id"] == str(user_id)
        assert data["text"] == answer_data["text"]
        assert data["question_id"] == question.id
        assert "created_at" in data


class TestGetAnswerById(BaseTestCase):
    url = "/answers/{id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        question = await QuestionFactory.create_async(
            session=self.session, text="What is Python?"
        )
        user_id = uuid.uuid4()
        answer = await AnswerFactory.create_async(
            session=self.session,
            question_id=question.id,
            user_id=user_id,
            text="Python is a programming language",
        )

        response = await self.client.get(url=self.url.format(id=answer.id))

        data = await self.assert_response_ok(response=response)
        assert data["id"] == answer.id
        assert data["user_id"] == str(answer.user_id)
        assert data["text"] == answer.text
        assert data["question_id"] == answer.question_id
        assert "created_at" in data


class TestDeleteAnswer(BaseTestCase):
    url = "/answers/{id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        question = await QuestionFactory.create_async(
            session=self.session, text="What is Python?"
        )
        user_id = uuid.uuid4()
        answer = await AnswerFactory.create_async(
            session=self.session,
            question_id=question.id,
            user_id=user_id,
            text="Python is a programming language",
        )

        response = await self.client.delete(url=self.url.format(id=answer.id))

        await self.assert_response_no_content(response=response)
