from abc import abstractmethod

from src.auth.user_rep import UserRepository
from src.database import session


class UoWInterface:
    users: UserRepository

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UoW(UoWInterface):
    def __init__(self) -> None:
        self.sessionmaker = session

    async def __aenter__(self):
        self.session = self.sessionmaker()
        self.users = UserRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
