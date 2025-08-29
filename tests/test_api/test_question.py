import pytest

from tests.test_api.base import BaseTestCase


class TestUserMe(BaseTestCase):
    url = "/user/me"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        user, headers = await self.create_user_and_get_token()

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert data["id"] == user["id"]
        assert data["email"] == user["email"]
