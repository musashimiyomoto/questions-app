import uuid
from unittest import mock

import pytest

from settings import auth_settings
from tests.factories import UserFactory
from tests.test_api.base import BaseTestCase
from utils.crypto import pwd_context


class TestAuthRegister(BaseTestCase):
    url = "/auth/register"

    def _user_data(self) -> dict:
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.doe-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user_data = self._user_data()

        response = await self.client.post(url=self.url, json=user_data)

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert data["email"] == user_data["email"]
        assert data["is_active"] is False
        assert "created_at" in data
        assert "hashed_password" not in data
        assert "password" not in data


class TestAuthLogin(BaseTestCase):
    url = "/auth/login"

    def _user_data(self) -> dict:
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.doe-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user_data = self._user_data()
        await UserFactory.create_async(
            session=self.session,
            email=user_data["email"],
            hashed_password=pwd_context.hash(user_data["password"]),
        )

        response = await self.client.post(
            url=self.url,
            json={"email": user_data["email"], "password": user_data["password"]},
        )

        data = await self.assert_response_ok(response=response)
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == auth_settings.token_type


class TestAdminAuthSendEmailCode(BaseTestCase):
    url = "/auth/send/{email}/code"

    def _user_data(self) -> dict:
        return {
            "name": "John Doe",
            "email": f"john.doe-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user_data = self._user_data()
        await UserFactory.create_async(
            session=self.session,
            email=user_data["email"],
            hashed_password=pwd_context.hash(user_data["password"]),
            is_active=False,
        )

        response = await self.client.post(
            url=self.url.format(email=user_data["email"]),
        )

        await self.assert_response_no_content(response=response)


class TestAuthVerifyEmail(BaseTestCase):
    url = "/auth/verify/{email}/{code}"
    code = "123456"

    def _user_data(self) -> dict:
        return {
            "name": "John Doe",
            "email": f"john.doe-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure_password123",
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user_data = self._user_data()
        await UserFactory.create_async(
            session=self.session,
            email=user_data["email"],
            hashed_password=pwd_context.hash(user_data["password"]),
            is_active=False,
        )

        with mock.patch(
            "usecases.auth.AuthUsecase._generate_code", return_value=self.code
        ):
            await self.client.post(url=f"/auth/send/{user_data['email']}/code")
            response = await self.client.post(
                url=self.url.format(email=user_data["email"], code=self.code)
            )

        await self.assert_response_no_content(response=response)
