from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")


class BaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model]):
        self.model = model

    async def create(
        self, session: AsyncSession, data: dict[str, Any], *args, **kwargs
    ) -> Model:
        """Create a new model instance.

        Args:
            session: The async session.
            data: The data to create the model instance.

        Returns:
            The created model instance.

        """
        instance = self.model(**data)

        session.add(instance=instance)
        await session.commit()
        await session.refresh(instance)

        return instance

    async def get_all(self, session: AsyncSession, **filters) -> list[Model]:
        """Get all model instances.

        Args:
            session: The async session.
            **filters: The filters to apply to the query.

        Returns:
            The list of model instances.

        """
        result = await session.execute(
            statement=select(self.model).filter_by(**filters)
        )
        return list(result.scalars().all())

    async def get_by(self, session: AsyncSession, **filters) -> Model | None:
        """Get a model instance by filters.

        Args:
            session: The async session.
            **filters: The filters to apply to the query.

        Returns:
            The model instance.

        """
        result = await session.execute(
            statement=select(self.model).filter_by(**filters)
        )
        return result.scalar_one_or_none()

    async def update_by(
        self, session: AsyncSession, data: dict[str, Any], **filters
    ) -> Model | None:
        """Update a model instance by filters.

        Args:
            session: The async session.
            data: The data to update the model instance.
            **filters: The filters to apply to the query.

        Returns:
            The updated model instance.

        """
        instance = await self.get_by(session=session, **filters)

        if instance:
            for key, value in data.items():
                setattr(instance, key, value)

            await session.commit()
            await session.refresh(instance=instance)

        return instance

    async def delete_by(self, session: AsyncSession, **filters) -> bool:
        """Delete a model instance by filters.

        Args:
            session: The async session.
            **filters: The filters to apply to the query.

        Returns:
            True if the model instance was deleted, False otherwise.

        """
        instance = await self.get_by(session=session, **filters)

        if instance:
            await session.delete(instance=instance)
            await session.commit()

            return True

        return False
