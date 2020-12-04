from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Auth"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    REALM_APP_ID: str
    DB_URL: str
    DB_NAME: str


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    SECURE_COOKIE: bool = False


class Settings(CommonSettings, ServerSettings, DatabaseSettings, AuthSettings):
    pass


settings = Settings()
