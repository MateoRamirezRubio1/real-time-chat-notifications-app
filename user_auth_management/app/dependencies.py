from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from .db.session import SessionLocal, engine
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .core.security import decode_access_token, add_token_to_revoked_list
from .schemas.user import User
from .db.base import Base


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        yield db


db_dependency = get_db
    
def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
    
async def verify_token(token: str = Depends(get_token_from_cookie)) -> str:
    credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            raise credentials
        return email
    except JWTError as e:
        raise credentials


async def get_current_user(
    db: AsyncSession = Depends(db_dependency), token: str = Depends(get_token_from_cookie)
) -> User:
    from .services.user import get_user_by_email
    
    email = await verify_token(token)

    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def logout_for_actual_token(token: str = Depends(get_token_from_cookie), db: AsyncSession = Depends(db_dependency)):
    await add_token_to_revoked_list(db, token)

