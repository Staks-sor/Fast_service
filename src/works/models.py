from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Work(Base):
    __tablename__ = "work"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(70))
    description: Mapped[str] = mapped_column(Text())
    duration_in_minutes: Mapped[int]

    supplies: Mapped[list["Supply"]] = relationship(
        back_populates="works", secondary="work_supply"
    )


class Supply(Base):
    __tablename__ = "supply"

    title: Mapped[str] = mapped_column(String(70), primary_key=True)
    supply_type: Mapped[str] = mapped_column(String(50))
    amount: Mapped[int]
    works: Mapped[list["Work"]] = relationship(
        back_populates="supplies", secondary="work_supply"
    )


class WorkSupply(Base):
    __tablename__ = "work_supply"
    work_id: Mapped[UUID] = mapped_column(
        ForeignKey(Work.id), primary_key=True
    )
    supply_title: Mapped[str] = mapped_column(
        ForeignKey(Supply.title), primary_key=True
    )
