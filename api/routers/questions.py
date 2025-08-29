from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionListResponse
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[QuestionListResponse])
async def get_questions(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching all questions")
    result = await db.execute(select(Question).order_by(Question.created_at.desc()))
    questions = result.scalars().all()
    return questions


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question: QuestionCreate, 
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Creating new question: {question.text[:50]}...")
    
    db_question = Question(text=question.text)
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    
    logger.info(f"Created question with ID: {db_question.id}")
    return db_question


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching question with ID: {question_id}")
    
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.answers))
        .where(Question.id == question_id)
    )
    question = result.scalar_one_or_none()
    
    if not question:
        logger.warning(f"Question with ID {question_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting question with ID: {question_id}")
    
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    
    if not question:
        logger.warning(f"Question with ID {question_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    await db.delete(question)
    await db.commit()
    
    logger.info(f"Successfully deleted question with ID: {question_id}")
    return None
