from factory.declarations import LazyAttribute

from constants.text import DEFAULT_TEXT_LENGTH
from db.models import Question
from tests.factories.base import AsyncSQLAlchemyModelFactory, fake


class QuestionFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Question

    text = LazyAttribute(lambda obj: fake.text(max_nb_chars=DEFAULT_TEXT_LENGTH))
