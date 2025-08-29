from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db
from api.schemas import LoginSchema, TokenSchema, UserCreateSchema, UserResponseSchema
from settings import auth_settings

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(path="/login")
async def login(
    data: Annotated[LoginSchema, Body(description="Data for login")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[auth.AuthUsecase, Depends(dependency=auth.get_auth_usecase)],
) -> TokenSchema:
    return TokenSchema(
        access_token=await usecase.login(session=session, **data.model_dump()),
        token_type=auth_settings.token_type,
    )


@router.post(path="/register")
async def register(
    data: Annotated[UserCreateSchema, Body(description="User data for register")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[auth.AuthUsecase, Depends(dependency=auth.get_auth_usecase)],
) -> UserResponseSchema:
    return UserResponseSchema.model_validate(
        await usecase.register(session=session, **data.model_dump(exclude_none=True))
    )


@router.post(path="/send/{email}/code")
async def send_email_code(
    email: Annotated[str, Path(description="Email for sending code")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[auth.AuthUsecase, Depends(dependency=auth.get_auth_usecase)],
) -> JSONResponse:
    await usecase.send_email_code(session=session, email=email)
    return JSONResponse(
        content={"message": "Email code sent successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.post(path="/verify/{email}/{code}")
async def verify_email(
    email: Annotated[str, Path(description="Email for verification")],
    code: Annotated[str, Path(description="Code for verification")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[auth.AuthUsecase, Depends(dependency=auth.get_auth_usecase)],
) -> JSONResponse:
    await usecase.verify_email(session=session, email=email, code=code)
    return JSONResponse(
        content={"message": "Email verified successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
