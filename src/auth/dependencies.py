from typing import Annotated
from fastapi import Depends
from datetime import datetime

from src.auth.schemas import UserResponce
from src.uow import UoW, UoWInterface
from src.auth import utils
from src.auth.service import AuthService
from src.auth.models import User


UowDep = Annotated[UoW, Depends(UoW)]

oauth_scheme = utils.OAuthPasswordWithCookie("auth/login", auto_error=True)


async def get_current_user(
    uow: UowDep, token: str = Depends(oauth_scheme)
) -> UserResponce:
    payload = utils.decode_token(token, "access")
    user = await AuthService().get_user(payload.uuid, uow)
    return user
