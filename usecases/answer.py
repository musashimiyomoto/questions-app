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
        logger.info(f"⏲️ Creating answer for question {question_id} by user {user_id}")

        question = await self._question_repository.get_by(
            session=session, id=question_id
        )

        if not question:
            logger.error(f"❌ Question with ID {question_id} not found")
            raise QuestionNotFoundError

        answer = await self._answer_repository.create(
            session=session,
            data={"question_id": question_id, "user_id": user_id, "text": text},
        )

        logger.info(f"✅ Created answer with ID: {answer.id}")

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
        logger.info(f"⏲️ Fetching answer with ID: {id}")

        answer = await self._answer_repository.get_by(session=session, id=id)

        if not answer:
            logger.error(f"❌Answer with ID {id} not found")
            raise AnswerNotFoundError

        logger.info(f"✅ Fetched answer with ID: {answer.id}")

        return answer

    async def delete_by_id(self, session: AsyncSession, id: int) -> None:
        """Delete an answer by ID.

        Args:
            session: The session.
            id: The answer ID.

        Raises:
            AnswerNotFoundError: If the answer is not found.

        """
        logger.info(f"⏲️ Deleting answer with ID: {id}")

        result = await self._answer_repository.delete_by(session=session, id=id)

        if not result:
            logger.error(f"❌ Answer with ID {id} not found")
            raise AnswerNotFoundError

        logger.info(f"✅ Deleted answer with ID: {id}")
