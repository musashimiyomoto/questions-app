from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db.sessions import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get the session.

    Yields:
        The session.

    """
    async with async_session() as session:
        yield session
