from db.models import Answer
from db.repositories.base import BaseRepository


class AnswerRepository(BaseRepository[Answer]):
    def __init__(self):
        super().__init__(model=Answer)
