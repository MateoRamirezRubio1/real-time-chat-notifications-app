from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import user as userSchemas
from ..db.models import user as userModels
from ..core.security import get_password_hash, add_token_to_revoked_list
from sqlalchemy.future import select
from starlette import status
from fastapi import HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from ..dependencies import db_dependency, get_token_from_cookie


async def get_user_by_email(db: AsyncSession, user_email: str) -> userModels.User:
    try:
        query = select(userModels.User).where(userModels.User.email == user_email)
        result = await db.execute(query)
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error: " + str(e),
        )


async def create_user(
    db: AsyncSession, user: userSchemas.UserCreate
) -> userModels.User:
    if await get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    try:
        db_user = userModels.User(
            userName=user.userName,
            email=user.email,
            password=get_password_hash(user.password),
            description=user.description,
            is_active=False,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error: " + str(e),
        )


async def delete_user(db: AsyncSession, user_id: int):
    try:
        query = select(userModels.User).where(userModels.User.pk == user_id)
        result = await db.execute(query)
        user = result.scalars().first()
        if user:
            await db.delete(user)
            await db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error: " + str(e),
        )
    
async def handle_user_deletion(user: userModels.User, db: AsyncSession = Depends(db_dependency), token: str = Depends(get_token_from_cookie)):
    await add_token_to_revoked_list(db, token)

    await delete_user(db, user.pk)
