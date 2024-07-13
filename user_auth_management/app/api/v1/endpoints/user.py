from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.user import create_user, handle_user_deletion
from ....schemas.user import UserCreate, User
from ....dependencies import get_current_user, db_dependency
from ....core.config import settings
from starlette import status


router = APIRouter()

COOKIE_NAME = settings.COOKIE_NAME


@router.get(
    "/me",
    response_model=User,
    responses={
        200: {"description": "User details fetched successfully"},
    }
)
async def get_current_user_details(current_user: User = Depends(get_current_user)):
    """Obtiene los detalles del usuario actual."""
    return current_user


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully"},
    }
)
async def create_new_user(
    user_create: UserCreate, db: AsyncSession = Depends(db_dependency)
):
    """Crea un nuevo usuario en la base de datos."""
    return await create_user(db, user_create)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User deleted successfully"},
    }
)
async def delete_current_user(response: Response, db: AsyncSession = Depends(db_dependency), current_user: User = Depends(get_current_user)):
    """Elimina el usuario actual."""
    handle_user_deletion(current_user, db)

    response.delete_cookie(key=COOKIE_NAME, httponly=True, secure=True, samesite="strict")

    return {"message": "User deleted successfully"}
