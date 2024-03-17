from abc import ABC, abstractmethod
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def get_one(self):
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


class SQLAlchemyRepository(AbstractRepository):

    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.id)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_one(self, uow, id):
        query = select(self.model).where(self.model.id == id)  # type: ignore
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(self):
        query = select(self.model)  # type: ignore
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_one(self):
        pass

    async def delete_one(self, id):
        stmt = delete(self.model).where(self.model.id == id)  # type: ignore
        await self.session.execute(stmt)
