from pydantic_settings import BaseSettings, SettingsConfigDict
from passlib.context import CryptContext


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="src/auth/.env_auth", extra="allow")

    jwt_secret: str
    jwt_algorithm: str
    token_expiration_in_minutes: int


auth_settings = AuthSettings()  # type: ignore
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
