from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.postgres_dsn, echo=True)

session = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
