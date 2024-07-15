from fastapi import Depends, HTTPException, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from .db.session import SessionLocal, engine
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .core.security import (
    decode_access_token,
    add_token_to_revoked_list,
    check_token_revoked,
)
from .db.base import Base


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.

    This function yields a new database session for each request and closes the session when the request is done.
    It also ensures that the database schema is created or updated during startup.

    Returns:
        AsyncGenerator[AsyncSession, None]: An asynchronous generator yielding the database session.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        yield db

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
    """


db_dependency = get_db


def get_token_from_query_param(token: str) -> str:
    """
    Extracts the token from the query parameters.

    This function checks if the token is provided in the query parameters and raises an exception if it's missing.

    Args:
        token (str): The token from the query parameters.

    Returns:
        str: The token.

    Raises:
        HTTPException: Raises HTTP 401 if no token is found.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


async def verify_token(
    token: str = Depends(get_token_from_query_param),
    db: AsyncSession = Depends(db_dependency),
) -> str:
    """
    Verifies the provided JWT token.

    This function decodes the token, checks if it is revoked, and extracts the email from the token payload.

    Args:
        token (str): The JWT token from the query parameters.
        db (AsyncSession): The asynchronous database session.

    Returns:
        str: The email extracted from the token payload.

    Raises:
        HTTPException: Raises HTTP 401 for invalid or revoked tokens.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email or await check_token_revoked(db, token):
            raise credentials_exception

        return email
    except JWTError as e:
        raise credentials_exception


async def logout_for_actual_token(
    token: str = Depends(get_token_from_query_param),
    db: AsyncSession = Depends(db_dependency),
):
    """
    Handles logout by adding the token to the revoked list.

    This function verifies the provided token, and if it is valid, it adds the token to the revoked list.

    Args:
        token (str): The JWT token from the query parameters.
        db (AsyncSession): The asynchronous database session.
    """
    email = await verify_token(token, db)
    if email:
        await add_token_to_revoked_list(db, token)
