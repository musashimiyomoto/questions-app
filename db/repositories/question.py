from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Question
from db.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    def __init__(self):
        super().__init__(model=Question)

    async def get_with_answers(self, session: AsyncSession, id: int) -> Question | None:
        """Get a question with its answers.

        Args:
            session: The session.
            id: The question ID.

        Returns:
            The question.

        """
        result = await session.execute(
            statement=select(Question)
            .options(selectinload(Question.answers))
            .where(Question.id == id)
        )

        return result.scalar_one_or_none()
