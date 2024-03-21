from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import UowDep
from src.auth.schemas import UserCreateSchema, UserResponse
from src.auth.service import AuthService
from src.auth.dependencies import get_current_user

from src.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register_user(user: UserCreateSchema, uow: UowDep):
    await AuthService.add_user(user, uow)


@router.post("/login")
async def log_user_in(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    uow: UowDep,
):
    tokens = await AuthService.authenticate_user(credentials, uow)
    if tokens:
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            max_age=settings.access_token_expiration * 60,
            httponly=True,
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            max_age=settings.refresh_token_expiration * 60 * 60 * 24,
            httponly=True,
        )


@router.post("/refresh")
async def refresh_tokens(request: Request, response: Response, uow: UowDep):
    current_token = request.cookies.get("refresh_token")

    if not current_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    new_tokens = await AuthService.refresh_tokens(current_token, uow)

    response.set_cookie(
        key="access_token",
        value=new_tokens.access_token,
        max_age=settings.access_token_expiration * 60,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=new_tokens.refresh_token,
        max_age=settings.refresh_token_expiration * 60 * 60 * 24,
        httponly=True,
    )


@router.post("/abort")
async def abort_refresh_token(
    response: Response,
    uow: UowDep,
    user: UserResponse = Depends(get_current_user),
):
    await AuthService.abort_refresh_token(user.id, uow)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


@router.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    return user
