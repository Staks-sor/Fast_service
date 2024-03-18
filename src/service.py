from .uow import UoW


class Service:

    @classmethod
    def get_uow(cls) -> UoW:
        return UoW()
