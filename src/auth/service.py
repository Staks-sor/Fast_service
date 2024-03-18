from typing import NamedTuple
from datetime import datetime, UTC
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import UserCreateSchema, UserResponse
from src.auth.models import User
from src.auth import utils

from src.service import Service
from src.config import settings


class Tokens(NamedTuple):
    access_token: str
    refresh_token: str


class AuthService(Service):
    @classmethod
    async def add_user(cls, user: UserCreateSchema):
        user_dict = {"name": user.name, "email": user.email}
        hashed_pass = utils.hash_password(user.password)
        user_dict["hashed_password"] = hashed_pass

        async with cls.get_uow() as uow:
            await uow.users.add_one(user_dict)
            await uow.commit()

    @classmethod
    async def get_user(cls, uuid: str):
        async with cls.get_uow() as uow:
            user = await uow.users.get_one(User.id, uuid)
            return UserResponse.model_validate(user)

    @classmethod
    async def authenticate_user(cls, credentials: OAuth2PasswordRequestForm) -> Tokens:
        async with cls.get_uow() as uow:
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

    @classmethod
    async def refresh_tokens(cls, refresh_token: str):
        async with cls.get_uow() as uow:
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

    @classmethod
    async def abort_refresh_token(cls, user_id: UUID):
        async with cls.get_uow() as uow:
            await uow.users.update_one(User.id, user_id, refresh_token="")
            await uow.commit()
