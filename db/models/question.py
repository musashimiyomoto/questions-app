from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants.text import DEFAULT_TEXT_LENGTH
from db.models.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="ID"
    )

    text: Mapped[str] = mapped_column(
        String(length=DEFAULT_TEXT_LENGTH), nullable=False, comment="The text"
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), comment="Created at"
    )

    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )
