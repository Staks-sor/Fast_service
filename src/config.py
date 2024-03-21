from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="src/.env", extra="allow")

    postgres_password: str
    postgres_username: str
    postgres_host: str
    postgres_port: int
    postgres_db: str 
    postgres_test_db: str | None
    jwt_access_secret: str
    jwt_refresh_secret: str
    jwt_algorithm: str
    access_token_expiration: int
    refresh_token_expiration: int

    @property
    def postgres_dsn(self):
        return f"postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def TEST_POSTGRES_DSN(self):
         return f"postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_test_db}"


settings = Settings()  # type: ignore