from uuid import uuid4

import bcrypt
import jwt
import pytest
from faker import Faker
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.auth.models import User
from src.auth.schemas import UserCreateSchema
from src.auth.service import AuthService
from src.config import settings
from src.uow import UoW


class FakeUserModel(BaseModel):
    id: str
    hashed_password: str
    refresh_token: str = ""


uow = UoW()

fake = Faker()


class FakeUserRepository:
    model = User

    def __init__(self) -> None:
        self._users = {}

    async def add_one(self, usermodel: dict) -> None:
        user_id = usermodel["id"]
        self._users[user_id] = usermodel

    async def get_one(self, filter_by, filter_value):
        try:
            return self._users[filter_value]
        except KeyError:
            return None

    async def get_all(self):
        return list(self._users)

    async def update_one(self, filter_by, filter_value, **data):
        self._users[filter_value] = data

    async def delete_one(self, uuid: str):
        self._users[uuid] = None


class FakeUoW:

    def __init__(self) -> None:
        self._commit = False
        self.users = FakeUserRepository()

    async def commit(self):
        self._commit = True

    async def rollback(self): ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()


class TestAuthService:
    uow = FakeUoW()

    async def test_add_user(self):
        user_id = uuid4()
        user_name = fake.name()
        user_email = fake.email()
        user_password = fake.password()
        new_user = UserCreateSchema(
            id=user_id, name=user_name, email=user_email, password=user_password
        )

        await AuthService.add_user(new_user, self.uow)  # type: ignore

        assert len(self.uow.users._users) == 1
        assert self.uow.users._users[user_id]["name"] == user_name
        assert self.uow.users._users[user_id]["email"] == user_email
        encrypted_pass = self.uow.users._users[user_id]["hashed_password"]
        assert bcrypt.checkpw(new_user.password.encode(), encrypted_pass.encode())

    async def test_get_user(self):
        user_id = uuid4()
        user_name = fake.name()
        user_email = fake.email()
        created_user = {
            "id": user_id,
            "name": user_name,
            "email": user_email,
            "is_active": True,
        }
        self.uow.users._users[str(user_id)] = created_user

        user_from_service = await AuthService.get_user(str(user_id), self.uow)  # type: ignore
        assert user_from_service.id == user_id
        assert user_from_service.email == user_email
        assert user_from_service.name == user_name

    async def test_successful_authenticate_user(self):
        user_id = str(uuid4())
        user_name = fake.name()
        salt = bcrypt.gensalt()
        user_pass = "pass1234"
        user_pass_hashed = bcrypt.hashpw(user_pass.encode(), salt).decode()
        credentials = OAuth2PasswordRequestForm(username=user_name, password=user_pass)
        self.uow.users._users[user_name] = FakeUserModel(
            id=user_id, hashed_password=user_pass_hashed
        )

        tokens = await AuthService.authenticate_user(credentials, self.uow)  # type: ignore
        payload = jwt.decode(
            tokens.refresh_token, settings.jwt_refresh_secret, [settings.jwt_algorithm]
        )
        assert payload["uuid"] == user_id
        assert uow.commit

    async def test_fail_authenticate_user(self):
        with pytest.raises(HTTPException):
            credentials = OAuth2PasswordRequestForm(username="fake", password="pass")
            await AuthService.authenticate_user(credentials, self.uow)  # type: ignore
