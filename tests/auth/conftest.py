import pytest

from src.auth.models import User  # noqa: F401
from src.database import Base
from src.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import NullPool


engine = create_async_engine(settings.TEST_POSTGRES_DSN, poolclass=NullPool)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope='session')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)