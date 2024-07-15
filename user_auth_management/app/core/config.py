from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for configuring the application.

    Attributes:
    - DATABASE_URL (str): The URL for the database connection.
    - SECRET_KEY (str): The secret key used for encoding and decoding JWT tokens.
    - ALGORITHM (str): The algorithm used for hashing (e.g., HS256).
    - ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
    - COOKIE_NAME (str): The name of the cookie used to store the access token.
    """

    DATABASE_URL: str = (
        "mysql+aiomysql://root:password@localhost:3306/user_auth_management_db"
    )
    SECRET_KEY: str = "likeblogandstargit441"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    COOKIE_NAME: str = "access_token"

    class Config:
        """
        Configuration for the Settings class.

        Attributes:
        - case_sensitive (bool): Indicates if the settings should be case sensitive.
        """

        case_sensitive = True


# Instantiate the settings object
settings = Settings()
