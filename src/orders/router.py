from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
from src.auth.schemas import UserResponse
from src.dependencies import UowDep
from src.orders.schemas import CreateOrderSchema
from src.orders.service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/")
async def create_order(
    order: CreateOrderSchema,
    uow: UowDep,
    user: UserResponse = Depends(get_current_user),
):
    await OrderService.add_new_order(order, user.id, uow)
