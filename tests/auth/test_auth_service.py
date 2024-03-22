from datetime import datetime, timedelta
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

fake_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


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


@pytest.fixture(scope="function")
async def fake_uow():
    return FakeUoW()


class TestAuthService:
    async def test_add_user(self, fake_uow):
        user_id = uuid4()
        user_name = fake.name()
        user_email = fake.email()
        user_password = fake.password()
        new_user = UserCreateSchema(
            id=user_id, name=user_name, email=user_email, password=user_password
        )

        await AuthService.add_user(new_user, fake_uow)  # type: ignore

        assert len(fake_uow.users._users) == 1
        assert fake_uow.users._users[user_id]["name"] == user_name
        assert fake_uow.users._users[user_id]["email"] == user_email
        encrypted_pass = fake_uow.users._users[user_id]["hashed_password"]
        assert bcrypt.checkpw(new_user.password.encode(), encrypted_pass.encode())

    async def test_get_user(self, fake_uow):
        user_id = uuid4()
        user_name = fake.name()
        user_email = fake.email()
        created_user = {
            "id": user_id,
            "name": user_name,
            "email": user_email,
            "is_active": True,
        }
        fake_uow.users._users[str(user_id)] = created_user

        user_from_service = await AuthService.get_user(str(user_id), fake_uow)  # type: ignore
        assert user_from_service.id == user_id
        assert user_from_service.email == user_email
        assert user_from_service.name == user_name

    async def test_successful_authenticate_user(self, fake_uow):
        user_id = str(uuid4())
        user_name = fake.name()
        salt = bcrypt.gensalt()
        user_pass = "pass1234"
        user_pass_hashed = bcrypt.hashpw(user_pass.encode(), salt).decode()
        credentials = OAuth2PasswordRequestForm(username=user_name, password=user_pass)
        fake_uow.users._users[user_name] = FakeUserModel(
            id=user_id, hashed_password=user_pass_hashed
        )

        tokens = await AuthService.authenticate_user(credentials, fake_uow)  # type: ignore
        payload = jwt.decode(
            tokens.refresh_token, settings.jwt_refresh_secret, [settings.jwt_algorithm]
        )
        assert payload["uuid"] == user_id
        assert uow.commit

    async def test_fail_authenticate_user(self, fake_uow):
        with pytest.raises(HTTPException):
            credentials = OAuth2PasswordRequestForm(username="fake", password="pass")
            await AuthService.authenticate_user(credentials, fake_uow)  # type: ignore

    async def test_fake_refresh_tokens(self, fake_uow):
        with pytest.raises(HTTPException):
            await AuthService.refresh_tokens(fake_jwt_token, fake_uow)  # type: ignore

    async def test_expired_refresh_tokens(self, fake_uow):
        local_uow = FakeUoW()
        user_id = uuid4()
        expiration = datetime.now() - timedelta(days=1)
        user_dict = {"uuid": str(user_id), "exp": expiration}
        prepared_token = jwt.encode(user_dict, settings.jwt_refresh_secret)

        local_uow.users._users[prepared_token] = FakeUserModel(
            id=str(user_id), hashed_password="safssoiionsv"
        )

        with pytest.raises(HTTPException):
            await AuthService.refresh_tokens(prepared_token, local_uow)  # type: ignore

    async def test_no_refresh_token_in_storage(self, fake_uow):
        prepared_token = jwt.encode(
            {"uuid": str(uuid4()), "exp": datetime.now() + timedelta(days=1)},
            settings.jwt_refresh_secret,
        )
        fake_uow.users._users[prepared_token] = None

        with pytest.raises(HTTPException):
            await AuthService.refresh_tokens(prepared_token, fake_uow)

    async def test_successful_refresh_tokens(self, fake_uow, refresh_token):
        user_id = refresh_token[1]
        fake_uow.users._users[user_id] = FakeUserModel(
            id="unknown", hashed_password="strongly hashed"
        )

        tokens = await AuthService.refresh_tokens(refresh_token[0], fake_uow)

        access_payload = jwt.decode(
            tokens.access_token, settings.jwt_access_secret, [settings.jwt_algorithm]
        )

        refresh_payload = jwt.decode(
            tokens.refresh_token, settings.jwt_refresh_secret, [settings.jwt_algorithm]
        )

        assert (
            datetime.now().minute - datetime.fromtimestamp(access_payload["exp"]).minute
            <= settings.access_token_expiration
        )

        assert (
            datetime.now().day - datetime.fromtimestamp(refresh_payload["exp"]).day
            <= settings.refresh_token_expiration
        )

    async def test_abort_token(self, fake_uow):
        fake_record = fake.name()
        user_id = uuid4()
        fake_uow.users._users[str(user_id)] = fake_record

        await AuthService.abort_refresh_token(user_id, fake_uow)
        assert fake_uow.users._users[user_id]["refresh_token"] is None
