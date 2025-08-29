from http import HTTPStatus


class BaseError(Exception):
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
