from factory.declarations import LazyAttribute

from constants.text import DEFAULT_TEXT_LENGTH
from db.models import Answer
from tests.factories.base import AsyncSQLAlchemyModelFactory, fake


class AnswerFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Answer

    user_id = LazyAttribute(lambda obj: fake.uuid4())
    question_id = LazyAttribute(lambda obj: fake.pyint())
    text = LazyAttribute(lambda obj: fake.text(max_nb_chars=DEFAULT_TEXT_LENGTH))
