from db.models import Question
from db.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    def __init__(self):
        super().__init__(model=Question)
