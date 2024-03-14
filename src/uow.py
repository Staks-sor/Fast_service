from src.database import session
from src.auth.user_rep import UserRepository
from abc import ABC, abstractmethod


class UoWInterface(ABC):
    users: UserRepository

    @abstractmethod
    async def __aenter__():
        raise NotImplementedError

    @abstractmethod
    async def __aexit__():
        raise NotImplementedError

    @abstractmethod
    async def commit():
        raise NotImplementedError

    @abstractmethod
    async def rollback():
        raise NotImplementedError


class UoW(UoWInterface):
    def __init__(self) -> None:
        self.sessionmaker = session

    async def __aenter__(
        self,
    ):
        self.session = self.sessionmaker()
        self.users = UserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
