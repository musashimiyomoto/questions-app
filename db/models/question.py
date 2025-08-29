from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="ID"
    )

    text: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )
