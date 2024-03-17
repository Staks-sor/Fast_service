from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status

from src.auth.dependencies import UowDep
from src.auth.schemas import UserCreateSchema, UserResponce
from src.auth.service import AuthService
from src.auth.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from src.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register_user(user: UserCreateSchema, uow: UowDep):
    service = AuthService()
    await service.add_user(user, uow)  # type: ignore


@router.post("/login")
async def log_user_in(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    responce: Response,
    uow: UowDep,
):
    tokens = await AuthService().authenticate_user(credentials, uow)  # type: ignore
    if tokens:
        responce.set_cookie(
            key="access_token",
            value=tokens.access_token,
            max_age=settings.access_token_expiration * 60,
            httponly=True,
        )
        responce.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            max_age=settings.refresh_token_expiration * 60 * 60 * 24,
            httponly=True,
        )


@router.post("/refresh")
async def refresh_tokens(request: Request, responce: Response, uow: UowDep):
    current_token = request.cookies.get("refresh_token")
    print(current_token)
    if not current_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    new_tokens = await AuthService().refresh_tokens(current_token, uow)
    responce.set_cookie(
        key="access_token",
        value=new_tokens.access_token,
        max_age=settings.access_token_expiration * 60,
        httponly=True,
    )
    responce.set_cookie(
        key="refresh_token",
        value=new_tokens.refresh_token,
        max_age=settings.refresh_token_expiration * 60 * 60 * 24,
        httponly=True,
    )


@router.post("/abort")
async def abort_refresh_token(
    uow: UowDep,
    responce: Response,
    user: UserResponce = Depends(get_current_user),
):
    await AuthService().abort_refresh_token(user.id, uow)
    responce.delete_cookie("access_token")
    responce.delete_cookie("refresh_token")


@router.get("/me", response_model=UserResponce)
async def get_me(user=Depends(get_current_user)):
    return user
