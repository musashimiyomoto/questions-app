from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.answer import Answer
from app.models.question import Question
from app.schemas.answer import AnswerCreate, AnswerResponse
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["answers"])


@router.post("/questions/{question_id}/answers/", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
async def create_answer(
    question_id: int,
    answer: AnswerCreate,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Creating answer for question {question_id} by user {answer.user_id}")
    
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    
    if not question:
        logger.warning(f"Question with ID {question_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    db_answer = Answer(
        question_id=question_id,
        user_id=answer.user_id,
        text=answer.text
    )
    db.add(db_answer)
    await db.commit()
    await db.refresh(db_answer)
    
    logger.info(f"Created answer with ID: {db_answer.id}")
    return db_answer


@router.get("/answers/{answer_id}", response_model=AnswerResponse)
async def get_answer(answer_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching answer with ID: {answer_id}")
    
    result = await db.execute(select(Answer).where(Answer.id == answer_id))
    answer = result.scalar_one_or_none()
    
    if not answer:
        logger.warning(f"Answer with ID {answer_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    return answer


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(answer_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting answer with ID: {answer_id}")
    
    result = await db.execute(select(Answer).where(Answer.id == answer_id))
    answer = result.scalar_one_or_none()
    
    if not answer:
        logger.warning(f"Answer with ID {answer_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    await db.delete(answer)
    await db.commit()
    
    logger.info(f"Successfully deleted answer with ID: {answer_id}")
    return None
