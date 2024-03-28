from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from src.orders.models import Order
from src.repository import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository[Order]):
    model = Order

    async def get_orders_by_user_id(
        self, user_id: str | UUID
    ) -> Sequence[Order]:
        query = select(self.model).where(self.model.user_id == user_id)

        result = await self.session.execute(query)
        return result.scalars().all()
