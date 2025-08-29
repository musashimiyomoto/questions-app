import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants.text import DEFAULT_TEXT_LENGTH
from db.models.base import Base


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="ID"
    )

    user_id: Mapped[uuid.UUID] = mapped_column(nullable=False, comment="The user ID")
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        comment="The question ID",
    )

    text: Mapped[str] = mapped_column(
        String(length=DEFAULT_TEXT_LENGTH), nullable=False, comment="The text"
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), comment="Created at"
    )

    question = relationship("Question", back_populates="answers")
