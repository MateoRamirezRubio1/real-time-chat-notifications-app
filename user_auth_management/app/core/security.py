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

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    hashed_password = bcrypt_context.hash(password)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        is_correct_password = bcrypt_context.verify(plain_password, hashed_password)
        return is_correct_password
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during verifying password",
        )


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
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
    """Agrega un token a la lista de tokens revocados."""
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
    """Verifica si un token está en la lista de tokens revocados."""
    try:
        query = select(RevokedToken).where(RevokedToken.token == token)
        result = await db.execute(query)
        return True if result.scalars().first() else None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error checking if token is revoked",
        )
