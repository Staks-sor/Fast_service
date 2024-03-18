from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateSchema(BaseModel):
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
