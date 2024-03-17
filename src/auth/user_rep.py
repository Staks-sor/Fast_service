from src.auth.models import User
from src.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    model = User
    pass
