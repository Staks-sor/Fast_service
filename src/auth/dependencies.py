from typing import Annotated
from fastapi import Depends, HTTPException, status
from datetime import datetime
from src.auth.schemas import UserResponse
from src.uow import UoW, UoWInterface
from src.auth import utils
from src.auth.service import AuthService

UowDep = Annotated[UoWInterface, Depends(UoW)]

oauth_scheme = utils.OAuthPasswordWithCookie("auth/login", auto_error=True)


async def get_current_user(token: str = Depends(oauth_scheme)) -> UserResponse:
    payload = utils.decode_token(token, "access")
    if payload.exp < datetime.now():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="not authenticated")
    user = await AuthService.get_user(payload.uuid)
    return user
