from src.auth.schemas import UserCreateSchema
from src.uow import UoW
from src.auth.config import bcrypt_context


class AuthService:
    async def add_user(self, user: UserCreateSchema, uow: UoW):
        user_dict = {"name": user.name, "email": user.email}
        hashed_pass = bcrypt_context.hash(user.password)
        user_dict["hashed_password"] = hashed_pass
        async with uow:
            await uow.users.add_one(user_dict)
            await uow.commit()
