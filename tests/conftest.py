from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.auth.models import User  # noqa: F401
from src.config import settings
from src.database import Base

engine = create_async_engine(settings.postgres_dsn, poolclass=NullPool)

session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
async def create_tables():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def access_token() -> tuple[str, str]:
    user_id = str(uuid4())
    payload = {
        "uuid": user_id,
        "exp": datetime.now(UTC) + timedelta(minutes=settings.access_token_expiration),
    }
    return jwt.encode(payload, settings.jwt_access_secret), user_id


@pytest.fixture(scope="function")
def refresh_token(access_token):
    _, user_id = access_token
    payload = {
        "uuid": user_id,
        "exp": datetime.now(UTC) + timedelta(days=settings.refresh_token_expiration),
    }
    return jwt.encode(
        payload, settings.jwt_refresh_secret, settings.jwt_algorithm
    ), user_id
