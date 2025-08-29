from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Question
from db.repositories import QuestionRepository
from exceptions import QuestionNotFoundError
from settings import get_logger

logger = get_logger(__name__)


class QuestionUsecase:
    def __init__(self):
        self._question_repository = QuestionRepository()

    async def get_all(self, session: AsyncSession) -> list[Question]:
        """Get all questions ordered by creation date.

        Args:
            session: The session.

        Returns:
            The list of questions.

        """
        logger.info("⏲️ Fetching all questions")

        questions = await self._question_repository.get_all(session=session)

        logger.info(f"✅ Fetched {len(questions)} questions")

        return questions

    async def create(self, session: AsyncSession, text: str) -> Question:
        """Create a new question.

        Args:
            session: The session.
            text: The question text.

        Returns:
            The created question.

        """
        logger.info(f"⏲️ Creating question: {text[:50]}...")

        question = await self._question_repository.create(
            session=session, data={"text": text}
        )

        logger.info(f"✅ Created question with ID: {question.id}")

        return question

    async def get_with_answers(self, session: AsyncSession, id: int) -> Question:
        """Get a question by ID with its answers.

        Args:
            session: The session.
            id: The question ID.

        Returns:
            The question.

        Raises:
            QuestionNotFoundError: If the question is not found.

        """
        logger.info(f"⏲️ Fetching question with ID: {id}")

        question = await self._question_repository.get_with_answers(
            session=session, id=id
        )

        if not question:
            logger.error(f"❌ Question with ID {id} not found")
            raise QuestionNotFoundError

        logger.info(f"✅ Fetched question with ID: {id}")

        return question

    async def delete_by_id(self, session: AsyncSession, id: int) -> None:
        """Delete a question by ID.

        Args:
            session: The session.
            id: The question ID.

        Raises:
            QuestionNotFoundError: If the question is not found.

        """
        logger.info(f"⏲️ Deleting question and answers with ID: {id}")

        result = await self._question_repository.delete_by(session=session, id=id)

        if not result:
            logger.error(f"❌Question with ID {id} not found")
            raise QuestionNotFoundError

        logger.info(f"✅ Deleted question and answers with ID: {id}")
