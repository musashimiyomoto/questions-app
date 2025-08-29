from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db
from api.schemas import UserResponseSchema
from usecases import AuthUsecase

security = HTTPBearer()


def verify_credentials(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(dependency=security)],
) -> None:
    """Verify credentials.

    Args:
        credentials: The credentials.

    """
    AuthUsecase().verify_token(token=credentials.credentials)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(dependency=security)],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
) -> UserResponseSchema:
    """Get the current client.

    Dependencies:
        credentials: The credentials.
        session: The session.

    Returns:
        The current client.

    """
    return UserResponseSchema.model_validate(
        await AuthUsecase().get_current(token=credentials.credentials, session=session)
    )


def get_auth_usecase() -> AuthUsecase:
    """Get the user auth usecase.

    Returns:
        The user auth usecase.

    """
    return AuthUsecase()
