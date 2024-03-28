from src.masters.models import Master
from src.masters.schemas import MasterCreateSchema
from src.uow import UoWInterface


class MasterService:
    @classmethod
    async def add_new_master(
        cls, master: MasterCreateSchema, uow: UoWInterface
    ):
        async with uow:
            master_id = await uow.masters.add_one(
                master.model_dump(), Master.id
            )
            await uow.commit()
            return master_id
