from ..core.config import settings
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from starlette import status
from ..db.models.token import RevokedToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

# Configuration for JWT tokens and password hashing
SECRET_KEY = (
    settings.SECRET_KEY
)  # The secret key used for encoding and decoding JWT tokens
ALGORITHM = settings.ALGORITHM  # The algorithm used for hashing (e.g., HS256)
ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)  # Token expiration time in minutes

# Password hashing context for bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Args:
    - password (str): The plain password to be hashed.

    Returns:
    - str: The hashed password.

    Raises:
    - HTTPException: If there is an error during the hashing process.
    """
    hashed_password = bcrypt_context.hash(password)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
    - plain_password (str): The plain password to verify.
    - hashed_password (str): The hashed password to verify against.

    Returns:
    - bool: True if the password is correct, False otherwise.

    Raises:
    - HTTPException: If there is an error during the verification process.
    """
    try:
        is_correct_password = bcrypt_context.verify(plain_password, hashed_password)
        return is_correct_password
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during verifying password",
        )


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a new access token.

    Args:
    - data (dict): The payload data for the token.
    - expires_delta (timedelta | None): Optional expiration time for the token.

    Returns:
    - str: The encoded JWT token.

    Raises:
    - HTTPException: If there is an error during the token creation process.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    try:
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return encode_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode an access token and return the payload.

    Args:
    - token (str): The JWT token to decode.

    Returns:
    - dict: The decoded payload of the token.

    Raises:
    - HTTPException: If the token is invalid or decoding fails.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def add_token_to_revoked_list(db: AsyncSession, token: str):
    """
    Add a token to the revoked tokens list.

    Args:
    - db (AsyncSession): The database session.
    - token (str): The token to revoke.

    Raises:
    - HTTPException: If there is an error adding the token to the revoked list.
    """
    revoked_token = RevokedToken(token=token)
    db.add(revoked_token)
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding token to revoked list: " + e,
        )


async def check_token_revoked(db: AsyncSession, token: str) -> bool:
    """
    Check if a token is in the revoked tokens list.

    Args:
    - db (AsyncSession): The database session.
    - token (str): The token to check.

    Returns:
    - bool: True if the token is revoked, False otherwise.

    Raises:
    - HTTPException: If there is an error checking the token's status.
    """
    try:
        query = select(RevokedToken).where(RevokedToken.token == token)
        result = await db.execute(query)
        return True if result.scalars().first() else None
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error checking if token is revoked" + e,
        )
