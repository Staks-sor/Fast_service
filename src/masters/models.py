from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Master(Base):
    __tablename__ = "master"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    s_name: Mapped[str] = mapped_column(String(50), nullable=False)
    speciality: Mapped[str]
    experience: Mapped[int] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="master")  # type: ignore  # noqa: F821
