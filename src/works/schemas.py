from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class CreateWorkSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    duration_in_minutes: int
    supplies: list[str]


class CreateSupplySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    supply_type: str
    amount: int


class WorkResponceSchema(CreateWorkSchema):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    supplies: list[Optional[CreateSupplySchema]] = []


list_of_works = TypeAdapter(list[WorkResponceSchema])
list_of_supplies = TypeAdapter(list[CreateSupplySchema])


class SupplyResponceSchema(CreateSupplySchema):
    works: list[WorkResponceSchema]


class WorkCreatedSchema(BaseModel):
    work_id: str
