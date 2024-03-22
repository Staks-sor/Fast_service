from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def get_one(self, filter_by, filter_value):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, Generic[ModelType]):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, data: dict[str, Any]):
        stmt = insert(self.model).values(**data).returning(self.model.id)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_one(self, filter_by, filter_value) -> ModelType | None:
        query = select(self.model).where(filter_by == filter_value)  # type: ignore
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[ModelType]:
        query = select(self.model)  # type: ignore
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_one(self, filter_by, filter_value, **new_data):
        stmt = (
            update(self.model).where(filter_by == filter_value).values(**new_data)  # type: ignore
        )
        await self.session.execute(stmt)

    async def delete_one(self, id):
        stmt = delete(self.model).where(self.model.id == id)  # type: ignore
        await self.session.execute(stmt)
