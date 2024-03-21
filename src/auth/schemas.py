from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreateSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: EmailStr
    password: str


class UserToken(BaseModel):
    uuid: str
    exp: datetime


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    id: UUID
    name: str
    email: EmailStr
    is_active: bool
