from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.security import verify_password, create_access_token
from ..services.user import get_user_by_email
from ..schemas.user import User
from ..schemas.auth import Token
from ..core.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


async def authenticate_user(db: AsyncSession, email: str, password: str) -> None | User:
    """
    Authenticate a user by verifying the provided password.

    This function retrieves the user by their email and checks if the provided password matches
    the stored password in the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        email (str): The user's email address.
        password (str): The password provided by the user.

    Returns:
        User | None: The authenticated user if the password is correct; otherwise, `None`.

    Raises:
        HTTPException: Raises HTTP 500 exception if there is an error during authentication.
    """
    try:
        user = await get_user_by_email(db, email)
        if user and verify_password(password, user.password):
            return user
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during user authentication",
        )


async def login_for_access_token(db: AsyncSession, email: str, password: str) -> Token:
    """
    Perform user login and generate an access token.

    This function uses `authenticate_user` to verify the user's credentials. If the user is successfully authenticated,
    it generates a JWT access token that can be used for future API requests.

    Args:
        db (AsyncSession): The asynchronous database session.
        email (str): The user's email address.
        password (str): The password provided by the user.

    Returns:
        Token: A `Token` object containing the access token and token type.

    Raises:
        HTTPException: Raises HTTP 401 exception if the email or password is incorrect.
    """
    user = await authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
