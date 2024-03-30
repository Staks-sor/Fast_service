from fastapi import APIRouter, status

from src.dependencies import UowDep
from src.errors.schema import ErrorSchema
from src.works.schemas import (
    CreateSupplySchema,
    CreateWorkSchema,
    WorkCreatedSchema,
    WorkResponceSchema,
)
from src.works.service import SupplyService, WorkService

work_router = APIRouter(prefix="", tags=["works"])


@work_router.post(
    "/works",
    responses={
        status.HTTP_201_CREATED: {"model": WorkCreatedSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def add_new_work(work_schema: CreateWorkSchema, uow: UowDep):
    """creeates new work with provided supplies ids"""
    work_id = await WorkService.add_work(work_schema, uow)
    if work_id:
        return WorkCreatedSchema(work_id=work_id)


@work_router.get("/works")
async def get_all_works(uow: UowDep):
    works = await WorkService.get_all_works(uow)
    return works


@work_router.get("/works/{work_id}", response_model=WorkResponceSchema)
async def get_work_by_id(work_id: str, uow: UowDep):
    """returns all available works with required supplies"""
    result = await WorkService.get_one_work(work_id, uow)
    return result


@work_router.post("/supplies")
async def add_new_supply(supply_schema: CreateSupplySchema, uow: UowDep):
    new_supply_title = await SupplyService.add_supply(supply_schema, uow)
    return {"supply title": new_supply_title}


@work_router.get("/supplies/", response_model=list[CreateSupplySchema])
async def get_all_supplies(uow: UowDep, offset: int, limit: int):
    return await SupplyService.get_all_supplies(uow, limit, offset)
