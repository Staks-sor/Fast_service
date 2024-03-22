from dataclasses import dataclass
from uuid import uuid4

import bcrypt
import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from main import get_app
from tests.conftest import session_maker

fake = Faker()


@dataclass
class UserModel:
    id: str
    name: str
    email: str
    hashed_password: str
    is_active: bool
    is_admin: bool
    refresh_token: str


@pytest.fixture
def password():
    return fake.password()


@pytest.fixture
def hashed_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


@pytest.fixture
def created_user(hashed_password, refresh_token):
    refresh_token, user_id = refresh_token
    return UserModel(
        id=user_id,
        name=fake.name(),
        email=fake.email(),
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False,
        refresh_token=refresh_token[0],
    )


@pytest.fixture(scope="session")
def app():
    return get_app()


@pytest.fixture(scope="function")
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://localhost:8000"
    ) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def inserted_user(create_tables, created_user):
    query_params = {
        "id": created_user.id,
        "name": created_user.name,
        "email": created_user.email,
        "hashed_password": created_user.hashed_password,
        "is_admin": created_user.is_active,
        "is_active": created_user.is_admin,
        "refresh_token": created_user.refresh_token,
    }
    print(created_user.refresh_token)
    query = text(
        """insert into "user"(id, name, email, hashed_password, is_admin, is_active, refresh_token) 
        values(:id, :name, :email, :hashed_password, :is_admin, :is_active, :refresh_token)"""
    )
    async with session_maker() as session:
        await session.execute(query, query_params)
        await session.commit()


async def test_successful_register_user(create_tables, client):
    user_name = fake.name()
    user_email = fake.email()
    user_pass = fake.password()
    responce = await client.post(
        "/auth/register",
        json={"name": user_name, "email": user_email, "password": user_pass},
    )

    assert responce.status_code == 200
    async with session_maker() as session:
        query = text('select * from "user" where email = :email;')
        result = await session.execute(query, {"email": user_email})
        row = result.one_or_none()
        assert user_email in row
        assert user_name in row
        assert bcrypt.checkpw(user_pass.encode(), row[3].encode())  # type: ignore


async def test_invalid_email_register(create_tables, client):
    user_name = fake.name()
    user_email = "wrongemail"
    user_pass = fake.password()

    responce = await client.post(
        "/auth/register",
        json={"name": user_name, "email": user_email, "password": user_pass},
    )
    assert responce.status_code == 422


async def test_successful_login(
    create_tables, client, inserted_user, password, created_user
):
    form_data = {
        "username": created_user.email,
        "password": password,
    }
    responce = await client.post("/auth/login", data=form_data)
    assert responce.status_code == 200
    assert responce.cookies.get("access_token") is not None
    assert responce.cookies.get("refresh_token") is not None


async def test_successful_refresh_tokens(
    create_tables, access_token, refresh_token, client, inserted_user, created_user
):
    client.cookies.set("access_token", access_token[0])
    client.cookies.set("refresh_token", refresh_token[0])
    print(refresh_token[0])
    print(client.cookies.get("refresh_token"))
    responce = await client.post("/auth/refresh")
    assert responce.status_code == 200


async def test_without_token_refresh_tokens(create_tables, client):
    responce = await client.post("/auth/refresh")

    assert responce.status_code == 401


async def test_abort_tokens(
    create_tables, inserted_user, client, refresh_token, access_token
):
    refr_token, user_id = refresh_token
    client.cookies.set("access_token", access_token[0])
    client.cookies.set("refresh_token", refr_token)

    responce = await client.post("/auth/abort")
    assert responce.status_code == 200
    assert responce.cookies.get("refresh_token") is None
    assert responce.cookies.get("access_token") is None
