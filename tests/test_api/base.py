from http import HTTPStatus

import pytest_asyncio
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession


class BaseTestCase:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, test_session: AsyncSession, test_client: AsyncClient):
        self.session = test_session
        self.client = test_client

    async def assert_response_ok(self, response: Response) -> dict:
        assert response.status_code == HTTPStatus.OK
        return response.json()

    async def assert_response_no_content(self, response: Response) -> None:
        assert response.status_code in [
            HTTPStatus.NO_CONTENT,
            HTTPStatus.ACCEPTED,
            HTTPStatus.CREATED,
        ]

    async def assert_response_not_found(self, response: Response) -> dict:
        assert response.status_code == HTTPStatus.NOT_FOUND
        return response.json()
