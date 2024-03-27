from fastapi import APIRouter

from src.dependencies import UowDep
from src.masters.schemas import MasterCreateSchema
from src.masters.service import MasterService

router = APIRouter(prefix="/masters", tags=["masters"])


@router.post("/masters")
async def add_master(master: MasterCreateSchema, uow: UowDep):
    master_id = await MasterService.add_new_master(master, uow)
    return {"master id": master_id}
