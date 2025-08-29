from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Task
from db.repositories import TaskRepository
from enums import TaskStatus
from exceptions import TaskNotAvailableTransitionError, TaskNotFoundError


class TaskUsecase:
    def __init__(self):
        self._task_repository = TaskRepository()

    async def create(self, session: AsyncSession, data: dict) -> Task:
        """Create a new task.

        Args:
            session: The session.
            data: The task data.

        Returns:
            The created task.

        """
        return await self._task_repository.create(session=session, data=data)

    async def get_by(self, session: AsyncSession, **filters) -> Task:
        """Get a task by filters.

        Args:
            session: The session.
            **filters: The task filters.

        Returns:
            The task.

        """
        task = await self._task_repository.get_by(session=session, **filters)
        if not task:
            raise TaskNotFoundError

        return task

    async def get_all(self, session: AsyncSession, **filters) -> list[Task]:
        """Get all tasks.

        Args:
            session: The session.
            **filters: The task filters.

        Returns:
            The list of tasks.

        """
        return await self._task_repository.get_all(session=session, **filters)

    async def update_by(self, session: AsyncSession, data: dict, **filters) -> Task:
        """Update a task.

        Args:
            session: The session.
            data: The data to update.
            **filters: The task filters.

        Returns:
            The updated task.

        """
        task = await self._task_repository.update_by(
            session=session, data=data, **filters
        )
        if not task:
            raise TaskNotFoundError

        return task

    async def get_transitions(self, session: AsyncSession, id: int) -> list[TaskStatus]:
        """Get available transitions for task.

        Args:
            session: The session.
            id: The task ID.

        Returns:
            The list transitions.

        """
        task = await self.get_by(session=session, id=id)
        return task.status.transitions

    async def update_status(
        self, session: AsyncSession, id: int, status: TaskStatus
    ) -> Task:
        """Update task status.

        Args:
            session: The session.
            id: The task ID.
            status: The new task status.

        Returns:
            The updated task or None if not found.

        """
        if status not in await self.get_transitions(session=session, id=id):
            raise TaskNotAvailableTransitionError

        return await self.update_by(session=session, data={"status": status}, id=id)

    async def delete_by(self, session: AsyncSession, **filters) -> bool:
        """Delete a task.

        Args:
            session: The session.
            **filters: The task filters.

        Returns:
            True if the task was deleted, False otherwise.

        """
        return await self._task_repository.delete_by(session=session, **filters)
