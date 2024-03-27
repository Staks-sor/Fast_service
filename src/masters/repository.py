from src.masters.models import Master
from src.repository import SQLAlchemyRepository


class MasterRepository(SQLAlchemyRepository[Master]):
    model = Master
