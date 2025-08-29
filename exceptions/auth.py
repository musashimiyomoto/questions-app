from http import HTTPStatus

from exceptions.base import BaseError


class AuthError(BaseError):
    def __init__(self, message: str, status_code: HTTPStatus):
        super().__init__(message, status_code)


class AuthCredentialsError(AuthError):
    def __init__(
        self,
        message: str = "Could not validate credentials or user is inactive",
        status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED,
    ):
        super().__init__(message, status_code)
