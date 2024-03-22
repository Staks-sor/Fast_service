from uuid import uuid4

import pytest
from faker import Faker
from sqlalchemy import insert, select, text

from src.auth.models import User
from src.auth.schemas import UserCreateSchema
from src.auth.user_rep import UserRepository
from tests.conftest import session_maker

fake = Faker()


@pytest.fixture(scope="function")
async def inserted_user():
    user = {
        "id": str(uuid4()),
        "name": fake.name(),
        "email": fake.email(),
        "hashed_password": "SDLFVSDOIJFkmdsfa24",
    }
    async with session_maker() as session:
        stmt = insert(User).values(user)
        await session.execute(stmt)
        await session.commit()
    return user["id"]


@pytest.fixture(scope="function")
def users():
    users = [
        UserCreateSchema(name=fake.name(), email=fake.email(), password="pass1234"),
        UserCreateSchema(name=fake.name(), email=fake.email(), password="pass1234"),
        UserCreateSchema(name=fake.name(), email=fake.email(), password="pass1234"),
    ]
    return users


@pytest.fixture
async def inserted_users(create_tables):
    number_of_users = 3
    async with session_maker() as session:
        clean_up_table_stmt = text('truncate table "user";')
        await session.execute(clean_up_table_stmt)
        await session.commit()

        for i in range(number_of_users):
            stmt = insert(User).values(
                {
                    "name": fake.name(),
                    "email": fake.email(),
                    "hashed_password": fake.password(),
                }
            )
            await session.execute(stmt)
            await session.commit()
    return number_of_users


@pytest.mark.usefixtures("create_tables")
class TestUserRepsitory:
    async def test_add_user(self, users):
        async with session_maker() as s:
            for user in users:
                user_dict = user.model_dump(exclude="password")
                user_dict["hashed_password"] = "psdafasdf"
                await UserRepository(s).add_one(user_dict)

            stmt = text('select count(*) from "user";')
            res = await s.execute(stmt)

            assert len(users) == res.scalar_one()

    async def test_update_user(self, inserted_user):
        new_name = "georgiy"
        new_email = "georgiy@mail.com"

        async with session_maker() as session:
            await UserRepository(session).update_one(
                User.id, inserted_user, name=new_name, email=new_email
            )

            query = select(User).where(User.id == inserted_user)
            result = await session.execute(query)
            user = result.scalar_one()
            assert user.name == new_name
            assert user.email == new_email

    async def test_user_delete(self, inserted_user):
        async with session_maker() as session:
            await UserRepository(session).delete_one(inserted_user)

            query = select(User).where(User.id == inserted_user)
            result = await session.execute(query)

            assert result.scalar_one_or_none() is None

    async def test_get_all_users(self, inserted_users):
        async with session_maker() as session:
            users_in_repo = await UserRepository(session).get_all()

            assert len(users_in_repo) == inserted_users
