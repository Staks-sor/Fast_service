from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.postgres_dsn)

session = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
