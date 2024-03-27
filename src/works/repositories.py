from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.repository import SQLAlchemyRepository
from src.works.models import Supply, Work


class WorkRepository(SQLAlchemyRepository[Work]):
    model = Work

    async def get_work_with_required_supplies(
        self, work_id: str
    ) -> Work | None:
        query = (
            select(self.model)
            .where(self.model.id == work_id)
            .options(selectinload(self.model.supplies))
        )
        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_all_works_with_supplies(self):
        query = select(self.model).options(selectinload(self.model.supplies))
        result = await self.session.execute(query)
        return result.unique().scalars()

    async def add_supplies_to_work(
        self, work_id: str, supplies: Iterable[Supply]
    ):
        query = (
            select(self.model)
            .where(self.model.id == work_id)
            .options(selectinload(self.model.supplies))
        )
        query_result = await self.session.execute(query)
        work = query_result.scalar_one()
        for supply in supplies:
            work.supplies.append(supply)


class SupplyRepository(SQLAlchemyRepository[Supply]):
    model = Supply

    async def get_supply_with_work(self, supply_title) -> Supply | None:
        query = (
            select(self.model)
            .where(self.model.title == supply_title)
            .options(selectinload(self.model.works))
        )

        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_supplies_by_titles(self, titles: list[str]):
        query = select(self.model).where(self.model.title.in_(titles))
        result = await self.session.execute(query)
        return result.scalars().all()
