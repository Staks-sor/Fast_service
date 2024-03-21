from uuid import uuid4

import bcrypt
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import text

from main import get_app
from tests.conftest import session_maker


@pytest.fixture(scope="function")
def client():
    test_client = TestClient(get_app())
    yield test_client


fake = Faker()


@pytest.mark.skip
async def test_successful_register_user(create_tables, client):
    user_name = fake.name()
    user_email = fake.email()
    user_pass = fake.password()
    responce = client.post(
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

    responce = client.post(
        "/auth/register",
        json={"name": user_name, "email": user_email, "password": user_pass},
    )
    assert responce.status_code == 422


async def test_successful_login(create_tables, client):
    user_id = uuid4()
    user_name = fake.name()
    user_email = fake.email()
    user_password = fake.password()
    hashed_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()
    query_params = {
        "id": user_id,
        "name": user_name,
        "email": user_email,
        "hashed_password": hashed_password,
        "is_admin": False,
        "is_active": True,
    }
    form_data = {
        "username": user_email,
        "password": user_password,
    }
    async with session_maker() as session:
        stmt = text(
            """insert into "user"(id, name, email, hashed_password, is_admin, is_active) 
            values(:id, :name, :email, :hashed_password, :is_admin, :is_active);"""
        )
        await session.execute(stmt, query_params)
        await session.commit()

    responce = client.post("/auth/login", data=form_data)
    assert responce.status_code == 200
    assert responce.cookies.get("access_token") is not None
    assert responce.cookies.get("refresh_token") is not None
