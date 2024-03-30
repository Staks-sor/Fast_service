from uuid import UUID

from src.orders.models import Order
from src.orders.schemas import CreateOrderSchema
from src.uow import UoWInterface


class OrderService:
    @classmethod
    async def add_new_order(
        cls, order: CreateOrderSchema, user_id: UUID, uow: UoWInterface
    ):
        async with uow:
            new_order = order.model_dump(exclude={"works_ids"})
            new_order["user_id"] = user_id
            new_order["price"] = 0
            print(new_order)
            await uow.orders.add_one(new_order, Order.id)
            await uow.commit()
