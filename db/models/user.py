from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="ID"
    )

    email: Mapped[str] = mapped_column(comment="Email")
    hashed_password: Mapped[str | None] = mapped_column(comment="Hashed password")
    is_active: Mapped[bool] = mapped_column(default=True, comment="Is active")

    last_login: Mapped[datetime | None] = mapped_column(comment="Last login")

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), comment="Created at"
    )
