import pytest

from enums import TaskStatus
from tests.factories import TaskFactory
from tests.test_api.base import BaseTestCase


class TestTaskCreate(BaseTestCase):
    url = "/task"

    def _task_data(self) -> dict:
        return {
            "title": "Test Task",
            "description": "This is a test task",
            "status": TaskStatus.CREATED,
        }

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        task_data = self._task_data()
        _, headers = await self.create_user_and_get_token()

        response = await self.client.post(url=self.url, json=task_data, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert "id" in data
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert "created_at" in data
        assert "updated_at" in data


class TestTaskGetList(BaseTestCase):
    url = "/task/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        task_count = 3
        [
            await TaskFactory.create_async(session=self.session)
            for _ in range(task_count)
        ]
        _, headers = await self.create_user_and_get_token()

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == task_count


class TestTaskGetById(BaseTestCase):
    url = "/task/{id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        task = await TaskFactory.create_async(session=self.session)
        _, headers = await self.create_user_and_get_token()

        response = await self.client.get(
            url=self.url.format(id=task.id), headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == task.id
        assert data["title"] == task.title
        assert data["description"] == task.description
        assert data["status"] == task.status


class TestTaskUpdateById(BaseTestCase):
    url = "/task/{id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        task = await TaskFactory.create_async(session=self.session)
        update_data = {"title": "Updated Title", "description": "Updated description"}
        _, headers = await self.create_user_and_get_token()

        response = await self.client.patch(
            url=self.url.format(id=task.id), json=update_data, headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]


class TestTaskDeleteById(BaseTestCase):
    url = "/task/{id}"

    @pytest.mark.asyncio
    async def test_no_content(self) -> None:
        task = await TaskFactory.create_async(session=self.session)
        _, headers = await self.create_user_and_get_token()

        response = await self.client.delete(
            url=self.url.format(id=task.id), headers=headers
        )

        await self.assert_response_no_content(response=response)


class TestTaskGetTransitions(BaseTestCase):
    url = "/task/transitions/{id}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        task = await TaskFactory.create_async(
            session=self.session, status=TaskStatus.CREATED
        )
        _, headers = await self.create_user_and_get_token()

        response = await self.client.get(
            url=self.url.format(id=task.id), headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)


class TestTaskUpdateStatus(BaseTestCase):
    url = "/task/transitions/{id}/{status}"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        task = await TaskFactory.create_async(
            session=self.session, status=TaskStatus.CREATED
        )
        _, headers = await self.create_user_and_get_token()

        response = await self.client.patch(
            url=self.url.format(id=task.id, status=TaskStatus.IN_PROGRESS),
            headers=headers,
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == task.id
        assert data["status"] == TaskStatus.IN_PROGRESS
        assert data["title"] == task.title
        assert data["description"] == task.description
