from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.security import verify_password, create_access_token
from ..services.user import get_user_by_email
from ..schemas.user import User
from ..schemas.auth import Token
from ..core.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


async def authenticate_user(db: AsyncSession, email: str, password: str) -> None | User:
    """Autentica al usuario verificando la contraseña proporcionada."""
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
    user = await authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
