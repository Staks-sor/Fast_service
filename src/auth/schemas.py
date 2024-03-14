from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):

    name: str
    email: EmailStr
    password: str
