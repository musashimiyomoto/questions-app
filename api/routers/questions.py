from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db, question
from api.schemas import (
    QuestionCreateSchema,
    QuestionResponseSchema,
    QuestionWithAnswersResponseSchema,
)

router = APIRouter(tags=["Questions"])


@router.get(path="/questions/")
async def get_all(
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        question.QuestionUsecase, Depends(dependency=question.get_question_usecase)
    ],
) -> list[QuestionResponseSchema]:
    return [
        QuestionResponseSchema.model_validate(question)
        for question in await usecase.get_all(session=session)
    ]


@router.post(path="/questions/")
async def create(
    data: Annotated[
        QuestionCreateSchema, Body(description="Data for creating a question")
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        question.QuestionUsecase, Depends(dependency=question.get_question_usecase)
    ],
) -> QuestionResponseSchema:
    return QuestionResponseSchema.model_validate(
        await usecase.create(session=session, text=data.text)
    )


@router.get(path="/questions/{id}")
async def get_with_answers(
    id: Annotated[int, Path(description="Question ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        question.QuestionUsecase, Depends(dependency=question.get_question_usecase)
    ],
) -> QuestionWithAnswersResponseSchema:
    return QuestionWithAnswersResponseSchema.model_validate(
        await usecase.get_with_answers(session=session, id=id)
    )


@router.delete(path="/questions/{id}")
async def delete_by_id(
    id: Annotated[int, Path(description="Question ID")],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    usecase: Annotated[
        question.QuestionUsecase, Depends(dependency=question.get_question_usecase)
    ],
) -> JSONResponse:
    await usecase.delete_by_id(session=session, id=id)
    return JSONResponse(
        content={"message": "Question and answers deleted successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
