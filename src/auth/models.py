from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.database import Base
from uuid import UUID, uuid4


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(70), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    refresh_token: Mapped[str] = mapped_column(nullable=True)