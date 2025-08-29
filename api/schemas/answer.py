import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from constants.text import DEFAULT_TEXT_LENGTH


class AnswerBaseSchema(BaseModel):
    user_id: uuid.UUID = Field(default=..., description="The user ID")
    text: str = Field(
        default=...,
        description="The answer text",
        min_length=1,
        max_length=DEFAULT_TEXT_LENGTH,
    )


class AnswerCreateSchema(AnswerBaseSchema):
    pass


class AnswerUpdateSchema(BaseModel):
    text: str | None = Field(
        default=None,
        description="The new answer text",
        min_length=1,
        max_length=DEFAULT_TEXT_LENGTH,
    )


class AnswerResponseSchema(AnswerBaseSchema):
    id: int = Field(default=..., description="The answer ID", gt=0)
    question_id: int = Field(default=..., description="The question ID", gt=0)
    created_at: datetime = Field(default=..., description="The answer creation date")

    class Config:
        from_attributes = True
