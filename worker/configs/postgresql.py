from pydantic import BaseSettings, PostgresDsn


class PostgresSettings(BaseSettings):
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    POSTGRES_HOST: str

    class Config:
        env_file: str = ".env"

    @property
    def db_uri(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=f"/{self.POSTGRES_DATABASE}",
        )
