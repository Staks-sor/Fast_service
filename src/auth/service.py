from typing import NamedTuple
from uuid import UUID
from fastapi import HTTPException, status
from src.auth.schemas import UserCreateSchema, UserResponce
from src.uow import UoW, UoWInterface
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.models import User
from src.auth import utils
from src.config import settings
from datetime import datetime, UTC


class Tokens(NamedTuple):
    access_token: str
    refresh_token: str


class AuthService:
    async def add_user(self, user: UserCreateSchema, uow: UoW):
        user_dict = {"name": user.name, "email": user.email}
        print(user.password)
        hashed_pass = utils.hash_password(user.password)
        user_dict["hashed_password"] = hashed_pass
        async with uow:
            await uow.users.add_one(user_dict)
            await uow.commit()

    async def get_user(self, uuid: str, uow: UoW):
        async with uow:
            user = await uow.users.get_one(User.id, uuid)
            return UserResponce.model_validate(user)

    async def authenticate_user(
        self, credentials: OAuth2PasswordRequestForm, uow: UoW
    ) -> Tokens:
        async with uow:
            user = await uow.users.get_one(User.email, credentials.username)
            user_id = user.id
            if not utils.check_password(credentials.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid credentials",
                )
            access_token = utils.generate_token(
                str(user_id), settings.access_token_expiration, "access"
            )
            refresh_token = utils.generate_token(
                str(user_id), settings.refresh_token_expiration, "refresh"
            )
            await uow.users.update_one(User.id, user_id, refresh_token=refresh_token)
            await uow.commit()
            return Tokens(access_token, refresh_token)

    async def refresh_tokens(self, refresh_token: str, uow: UoW):
        async with uow:
            user = await uow.users.get_one(User.refresh_token, refresh_token)
            user_id = user.id
            if not user:
                raise HTTPException(
                    status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
                )
            payload = utils.decode_token(user.refresh_token, "refresh")
            if payload.exp < datetime.now(UTC):
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")
            new_access_token = utils.generate_token(
                str(user.id), settings.access_token_expiration, "access"
            )
            new_refresh_token = utils.generate_token(
                str(user.id), settings.refresh_token_expiration, "refresh"
            )
            await uow.users.update_one(
                User.id, user_id, refresh_token=new_refresh_token
            )
            await uow.commit()
            return Tokens(new_access_token, new_refresh_token)

    async def abort_refresh_token(self, user_id: UUID, uow: UoW):
        async with uow:
            await uow.users.update_one(User.id, user_id, refresh_token="")
            await uow.commit()
