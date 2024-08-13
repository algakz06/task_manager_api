from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl
from pydantic import computed_field, PostgresDsn

from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="UTF-8", case_sensitive=True
    )
    API_VERSION: str = "0.1.0"
    APP_NAME: str = "Banner Service"
    API_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    IMAGE_DIR: str = "images/"

    ADMIN_USERNAME: str
    ADMIN_PWD: str

    BROKER_URI: str = "redis://redis:6379"

    FACECLOUD_EMAIL: str
    FACECLOUD_PWD: str
    FACECLOUD_URL: str = "https://backend.facecloud.tevian.ru"

    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore
