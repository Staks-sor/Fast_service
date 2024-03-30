from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MasterCreateSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    s_name: str
    speciality: str
    experience: int
    phone_number: str = Field(min_length=7, max_length=20)
