from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.auth import utils
from src.auth.schemas import UserResponse
from src.auth.service import AuthService
from src.uow import UoW, UoWInterface

UowDep = Annotated[UoWInterface, Depends(UoW)]

oauth_scheme = utils.OAuthPasswordWithCookie("auth/login", auto_error=True)


async def get_current_user(
    uow: UowDep, token: str = Depends(oauth_scheme)
) -> UserResponse:
    payload = utils.decode_token(token, "access")
    if payload.exp < datetime.now(UTC):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="not authenticated")
    user = await AuthService.get_user(payload.uuid, uow)
    return user
