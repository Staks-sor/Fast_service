from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="src/.env", extra="allow")

    postgres_password: str
    postgres_username: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    @property
    def postgres_dsn(self):
        return f"postgresql+psycopg://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()  # type: ignore
