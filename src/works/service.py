from src.uow import UoWInterface
from src.works.models import Supply, Work, WorkSupply
from src.works.schemas import (
    CreateSupplySchema,
    CreateWorkSchema,
    WorkResponceSchema,
)


class WorkService:
    @classmethod
    async def add_work(cls, new_work: CreateWorkSchema, uow: UoWInterface):
        async with uow:
            supplies = await uow.supplies.get_supplies_by_titles(
                new_work.supplies
            )
            work_id = await uow.works.add_one(
                new_work.model_dump(exclude={"supplies"}), Work.id
            )

            await uow.works.add_supplies_to_work(work_id, supplies)
            await uow.commit()
            return str(work_id)

    @classmethod
    async def get_all_works(cls, uow: UoWInterface):
        async with uow:
            works = await uow.works.get_all_works_with_supplies()
            dto = [WorkResponceSchema.model_validate(work) for work in works]
            return dto

    @classmethod
    async def get_one_work(cls, work_id: str, uow: UoWInterface):
        async with uow:
            work = await uow.works.get_work_with_required_supplies(work_id)
            return WorkResponceSchema.model_validate(work)


class SupplyService:
    @classmethod
    async def add_supply(
        cls, new_supply: CreateSupplySchema, uow: UoWInterface
    ):
        async with uow:
            supply_title = await uow.supplies.add_one(
                new_supply.model_dump(), Supply.title
            )
            await uow.commit()
            return supply_title

    @classmethod
    async def get_all_supplies(
        cls, uow: UoWInterface, limit: int, offset: int
    ):
        async with uow:
            supplies = await uow.supplies.get_all(limit, offset)
            dto = [
                CreateSupplySchema.model_validate(supply)
                for supply in supplies
            ]

            return dto
