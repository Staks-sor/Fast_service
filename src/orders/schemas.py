from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CreateOrderSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    to_be_provided_at: datetime
    works_ids: list[UUID]
    master_id: UUID
