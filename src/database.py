from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

if settings.MODE == "DEV":
    engine = create_async_engine(settings.postgres_dsn, echo=True)
elif settings.MODE == "TEST":
    engine = create_async_engine(settings.postgres_dsn, poolclass=NullPool)

session = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

    def __repr__(self) -> str: ...
