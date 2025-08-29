import uuid
from http import HTTPStatus
from typing import AsyncGenerator
from unittest import mock

import pytest_asyncio
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from settings import auth_settings
from tests.factories import UserFactory
from utils.crypto import pwd_context


class BaseTestCase:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, test_session: AsyncSession, test_client: AsyncClient):
        self.session = test_session
        self.client = test_client

    @pytest_asyncio.fixture(autouse=True)
    async def _mock_smtp(self) -> AsyncGenerator[mock.MagicMock, None]:
        with mock.patch("smtplib.SMTP") as mock_smtp:
            mock_server = mock.MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            mock_smtp.return_value.__exit__.return_value = None
            yield mock_smtp

    @pytest_asyncio.fixture(autouse=True)
    async def _mock_redis(self) -> AsyncGenerator[mock.MagicMock, None]:
        redis_store = {}

        async def mock_get(name):
            return redis_store.get(name)

        async def mock_setex(name, time, value):
            redis_store[name] = value
            return "OK"

        with mock.patch("utils.redis.redis_client") as mock_redis:
            mock_redis.get.side_effect = mock_get
            mock_redis.setex.side_effect = mock_setex
            yield mock_redis

    async def assert_response_ok(self, response: Response) -> dict:
        assert response.status_code == HTTPStatus.OK
        return response.json()

    async def assert_response_no_content(self, response: Response) -> None:
        assert response.status_code in [
            HTTPStatus.NO_CONTENT,
            HTTPStatus.ACCEPTED,
            HTTPStatus.CREATED,
        ]

    async def create_user_and_get_token(
        self,
        email: str | None = None,
        password: str = "secure_password123",
    ) -> tuple[dict, dict]:
        if email is None:
            email = f"user-{uuid.uuid4().hex[:8]}@example.com"

        user = await UserFactory.create_async(
            session=self.session,
            email=email,
            hashed_password=pwd_context.hash(password),
        )

        response = await self.client.post(
            url="/auth/login", json={"email": email, "password": password}
        )

        return user.__dict__, {
            "Authorization": (
                f"{auth_settings.token_type} {response.json()['access_token']}"
            )
        }
