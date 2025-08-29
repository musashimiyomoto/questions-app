from factory.declarations import LazyAttribute

from db.models import Task
from enums import TaskStatus
from tests.factories.base import AsyncSQLAlchemyModelFactory, fake


class TaskFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Task

    title = LazyAttribute(lambda obj: fake.sentence(nb_words=3))
    description = LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    status = TaskStatus.CREATED
