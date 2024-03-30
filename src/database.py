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

    repr_num: int = 3
    repr_cols: tuple | tuple[str, ...] = ()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"{self.__class__.__name__}=({', '.join(cols)})"
