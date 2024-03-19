import pytest

from src.auth.models import User
from src.auth.schemas import UserCreateSchema
from src.auth.user_rep import UserRepository
from sqlalchemy import insert, text, select

from tests.auth.conftest import session_maker

@pytest.fixture
def user_dict_ready_for_insert():
    return {'id':'7d5d45d0-80e8-45fa-97d0-ed74f5ac0b85','name': 'german', 'email': 'german@mail.com', 'hashed_password': 'SDLFVSDOIJFkmdsfa24'}


@pytest.fixture
def users():
    users = [
        UserCreateSchema(name='vasyok', email='vasya@mail.com', password='pass1234'),
        UserCreateSchema(name='andrey', email='andr@mail.com', password='pass1234'),
        UserCreateSchema(name='kirill', email='kirill@mail.com', password='pass1234'),

    ]
    return users

@pytest.mark.usefixtures("create_tables")
async def test_add_user(users):
    async with session_maker() as s:
        for user in users:
            user_dict = user.model_dump(exclude='password')
            user_dict['hashed_password'] = 'psdafasdf'
            await UserRepository(s).add_one(user_dict)

        stmt = text('select count(*) from "user";')
        res = await s.execute(stmt)

        assert len(users) == res.scalar_one()


@pytest.mark.usefixtures("create_tables")
async def test_update_user(user_dict_ready_for_insert):
    new_name = 'georgiy'
    new_email = 'georgiy@mail.com'

    async with session_maker() as session:
        stmt = insert(User).values(user_dict_ready_for_insert)
        await session.execute(stmt)

        await UserRepository(session).update_one(
            User.name, 
            'german', 
            name=new_name, 
            email=new_email
            )
        
        query = select(User).where(User.id ==user_dict_ready_for_insert['id'])
        result = await session.execute(query)
        user = result.scalar_one()
        assert user.name == new_name
        assert user.email == new_email