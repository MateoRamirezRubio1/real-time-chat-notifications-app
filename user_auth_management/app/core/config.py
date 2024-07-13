from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "mysql+aiomysql://root:password@localhost:3306/user_auth_management_db"
    )
    SECRET_KEY: str = "likeblogandstargit441"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    COOKIE_NAME: str = "access_token"

    class Config:
        case_sensitive = True

settings = Settings()
