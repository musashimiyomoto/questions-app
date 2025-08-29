from datetime import datetime

from pydantic import BaseModel, Field

from api.schemas.answer import AnswerResponseSchema
from constants.text import DEFAULT_TEXT_LENGTH


class QuestionBaseSchema(BaseModel):
    text: str = Field(
        default=...,
        description="The question text",
        min_length=1,
        max_length=DEFAULT_TEXT_LENGTH,
    )


class QuestionCreateSchema(QuestionBaseSchema):
    pass


class QuestionUpdateSchema(BaseModel):
    text: str | None = Field(
        default=None,
        description="The new question text",
        min_length=1,
        max_length=DEFAULT_TEXT_LENGTH,
    )


class QuestionResponseSchema(QuestionBaseSchema):
    id: int = Field(default=..., description="The question ID", gt=0)
    created_at: datetime = Field(default=..., description="The question creation date")

    class Config:
        from_attributes = True


class QuestionWithAnswersResponseSchema(QuestionResponseSchema):
    answers: list[AnswerResponseSchema] = Field(
        default_factory=list, description="The question answers"
    )
