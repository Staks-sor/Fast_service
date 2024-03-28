from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.models import User
from src.database import Base


class OrderStatus(Enum):
    created = "created"
    acepted = "accepted"
    in_progress = "in_progress"
    finished = "finished"
    canceled = "canceled"


class Order(Base):
    __tablename__ = "order"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    price: Mapped[int]
    ordered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    to_be_provided_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[OrderStatus] = mapped_column(default="created")
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )
    master_id: Mapped[UUID] = mapped_column(ForeignKey("master.id"))

    master: Mapped["Master"] = relationship(back_populates="orders")  # type: ignore  # noqa: F821
    user: Mapped[User] = relationship(back_populates="orders")
    works: Mapped[list["Work"]] = relationship(  # type: ignore  # noqa: F821
        back_populates="orders", secondary="orders_works"
    )


class OrderWorks(Base):
    __tablename__ = "orders_works"
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("order.id"), primary_key=True
    )
    work_id: Mapped[UUID] = mapped_column(
        ForeignKey("work.id"), primary_key=True
    )
