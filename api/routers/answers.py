from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import answer, db
from api.schemas import AnswerCreateSchema, AnswerResponseSchema

router = APIRouter(tags=["Answers"])


@router.post("/questions/{id}/answers/")
async def create(
    id: Annotated[int, Path(description="Question ID")],
    data: Annotated[
        AnswerCreateSchema, Body(description="Data for creating an answer")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        answer.AnswerUsecase, Depends(dependency=answer.get_answer_usecase)
    ],
) -> AnswerResponseSchema:
    return AnswerResponseSchema.model_validate(
        await usecase.create(
            session=session, question_id=id, user_id=data.user_id, text=data.text
        )
    )


@router.get(path="/answers/{id}")
async def get_by_id(
    id: Annotated[int, Path(description="Answer ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        answer.AnswerUsecase, Depends(dependency=answer.get_answer_usecase)
    ],
) -> AnswerResponseSchema:
    return AnswerResponseSchema.model_validate(
        await usecase.get_by_id(session=session, id=id)
    )


@router.delete(path="/answers/{id}")
async def delete_by_id(
    id: Annotated[int, Path(description="Answer ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        answer.AnswerUsecase, Depends(dependency=answer.get_answer_usecase)
    ],
) -> JSONResponse:
    await usecase.delete_by_id(session=session, id=id)
    return JSONResponse(
        content={"message": "Answer deleted successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
