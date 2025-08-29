from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from api.schemas.answer import AnswerResponseSchema

class QuestionBaseSchema(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class QuestionCreateSchema(QuestionBaseSchema):
    pass


class QuestionUpdateSchema(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=1000)



class QuestionResponseSchema(QuestionBaseSchema):
    id: int
    created_at: datetime
    answers: List[AnswerResponseSchema] = []

    class Config:
        from_attributes = True


class QuestionListResponseSchema(QuestionBaseSchema):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
