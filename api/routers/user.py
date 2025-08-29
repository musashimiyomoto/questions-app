from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import auth
from api.schemas import UserResponseSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.get(path="/me")
async def get_me(
    current_user: Annotated[
        UserResponseSchema, Depends(dependency=auth.get_current_user)
    ],
) -> UserResponseSchema:
    return current_user
