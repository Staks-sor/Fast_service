from src.auth.models import User
from src.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
    pass
