from http import HTTPStatus

from exceptions.base import BaseError


class QuestionNotFoundError(BaseError):
    def __init__(
        self,
        message: str = "Question not found",
        status_code: HTTPStatus = HTTPStatus.NOT_FOUND,
    ):
        super().__init__(message=message, status_code=status_code)
