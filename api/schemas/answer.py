from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AnswerBaseSchema(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=255)
    text: str = Field(..., min_length=1, max_length=2000)


class AnswerCreateSchema(AnswerBaseSchema):
    pass


class AnswerUpdateSchema(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=2000)


class AnswerResponseSchema(AnswerBaseSchema):
    id: int
    question_id: int
    created_at: datetime

    class Config:
        from_attributes = True
