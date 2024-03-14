from fastapi import APIRouter

from src.auth.dependencies import UowDep
from src.auth.schemas import UserCreateSchema
from src.auth.service import AuthService


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register_user(user: UserCreateSchema, uow: UowDep):
    service = AuthService()
    await service.add_user(user, uow)  # type: ignore
