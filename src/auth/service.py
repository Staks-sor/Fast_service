from datetime import UTC, datetime
from typing import NamedTuple
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import utils
from src.auth.models import User
from src.auth.schemas import UserCreateSchema, UserResponse
from src.config import settings
from src.uow import UoWInterface


class Tokens(NamedTuple):
    access_token: str
    refresh_token: str


class AuthService:
    @classmethod
    async def add_user(cls, user: UserCreateSchema, uow: UoWInterface):
        user_dict = user.model_dump(exclude="password")  # type: ignore
        user_dict["hashed_password"] = utils.hash_password(user.password)

        async with uow:
            await uow.users.add_one(user_dict)
            await uow.commit()

    @classmethod
    async def get_user(cls, uuid: str, uow: UoWInterface):
        async with uow as uow:
            user = await uow.users.get_one(User.id, uuid)
            return UserResponse.model_validate(user)

    @classmethod
    async def authenticate_user(
        cls, credentials: OAuth2PasswordRequestForm, uow: UoWInterface
    ) -> Tokens:
        async with uow as uow:
            user = await uow.users.get_one(User.email, credentials.username)
            if not user or not utils.check_password(
                credentials.password, user.hashed_password
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid credentials",
                )
            user_id = user.id
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
    async def refresh_tokens(cls, refresh_token: str, uow: UoWInterface):
        payload = utils.decode_token(refresh_token, "refresh")
        user_id = payload.uuid
        async with uow as uow:
            user = await uow.users.get_one(User.id, user_id)
            if not user or payload.exp < datetime.now(UTC):
                raise HTTPException(
                    status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
                )
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
    async def abort_refresh_token(cls, user_id: UUID, uow: UoWInterface):
        async with uow as uow:
            await uow.users.update_one(User.id, user_id, refresh_token=None)
            await uow.commit()
