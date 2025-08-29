import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Answer
from db.repositories import AnswerRepository, QuestionRepository
from exceptions import AnswerNotFoundError, QuestionNotFoundError
from settings import get_logger

logger = get_logger(__name__)


class AnswerUsecase:
    def __init__(self):
        self._answer_repository = AnswerRepository()
        self._question_repository = QuestionRepository()

    async def create(
        self, session: AsyncSession, question_id: int, user_id: uuid.UUID, text: str
    ) -> Answer:
        """Create a new answer for a question.

        Args:
            session: The session.
            question_id: The question ID.
            user_id: The user ID.
            text: The answer text.

        Returns:
            The created answer.

        Raises:
            QuestionNotFoundError: If the question is not found.
            AnswerNotFoundError: If the answer is not found.

        """
        logger.info(
            "⏲️ Creating answer for question %s by user %s", question_id, user_id
        )

        question = await self._question_repository.get_by(
            session=session, id=question_id
        )

        if not question:
            logger.error("❌ Question with ID %s not found", question_id)
            raise QuestionNotFoundError

        answer = await self._answer_repository.create(
            session=session,
            data={"question_id": question_id, "user_id": user_id, "text": text},
        )

        logger.info("✅ Created answer with ID: %s", answer.id)

        return answer

    async def get_by_id(self, session: AsyncSession, id: int) -> Answer:
        """Get an answer by ID.

        Args:
            session: The session.
            id: The answer ID.

        Returns:
            The answer.

        Raises:
            AnswerNotFoundError: If the answer is not found.

        """
        logger.info("⏲️ Fetching answer with ID: %s", id)

        answer = await self._answer_repository.get_by(session=session, id=id)

        if not answer:
            logger.error("❌Answer with ID %s not found", id)
            raise AnswerNotFoundError

        logger.info("✅ Fetched answer with ID: %s", answer.id)

        return answer

    async def delete_by_id(self, session: AsyncSession, id: int) -> None:
        """Delete an answer by ID.

        Args:
            session: The session.
            id: The answer ID.

        Raises:
            AnswerNotFoundError: If the answer is not found.

        """
        logger.info("⏲️ Deleting answer with ID: %s", id)

        result = await self._answer_repository.delete_by(session=session, id=id)

        if not result:
            logger.error("❌ Answer with ID %s not found", id)
            raise AnswerNotFoundError

        logger.info("✅ Deleted answer with ID: %s", id)
