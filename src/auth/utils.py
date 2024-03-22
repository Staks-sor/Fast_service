from datetime import UTC, datetime, timedelta
from typing import Dict, Literal, Optional

import bcrypt
import jwt
from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2

from src.auth.schemas import UserToken
from src.config import settings


class OAuthPasswordWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str | None = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        pass_flow = OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes)
        flows = OAuthFlowsModel(password=pass_flow)
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    def __call__(self, request: Request) -> Optional[str]:
        authorization: str | None = request.cookies.get("access_token")
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
                )
            else:
                return None
        return authorization


def generate_token(user_uuid: str, expires_in: int, type: Literal["access", "refresh"]):
    expires = (
        timedelta(minutes=expires_in)
        if type == "access"
        else timedelta(days=expires_in)
    )
    payload = {"uuid": user_uuid, "exp": datetime.now(UTC) + expires}
    if type == "access":
        token = jwt.encode(payload, settings.jwt_access_secret, settings.jwt_algorithm)
    else:
        token = jwt.encode(payload, settings.jwt_refresh_secret, settings.jwt_algorithm)
    return token


def decode_token(token: str, type: Literal["access", "refresh"]):
    try:
        if type == "access":
            payload = jwt.decode(
                token, settings.jwt_access_secret, [settings.jwt_algorithm]
            )
        else:
            payload = jwt.decode(
                token, settings.jwt_refresh_secret, [settings.jwt_algorithm]
            )
    except jwt.InvalidTokenError as e:
        print(e, type)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid token"
        )
    return UserToken(
        uuid=payload["uuid"], exp=datetime.fromtimestamp(payload["exp"], UTC)
    )


def hash_password(password: str):
    password_encoded = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_encoded, salt=salt).decode()


def check_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
