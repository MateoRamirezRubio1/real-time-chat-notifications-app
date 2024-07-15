from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ....services.user import create_user, handle_user_deletion, get_current_user
from ....schemas.user import UserCreate, User
from ....dependencies import db_dependency
from ....core.config import settings
from starlette import status

# Create a new router instance
router = APIRouter()

# Retrieve cookie name from settings
COOKIE_NAME = settings.COOKIE_NAME


@router.get(
    "/me",
    response_model=User,
    responses={
        200: {"description": "User details fetched successfully"},
    },
)
async def get_current_user_details(
    token: str,
    db: AsyncSession = Depends(db_dependency),
):
    """
    Get details of the current authenticated user.

    Parameters:
    - token: str - The JWT token of the current user.
    - db: AsyncSession - The database session dependency.

    Returns:
    - User: The details of the current user.
    """
    current_user = await get_current_user(token, db)
    return current_user


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully"},
    },
)
async def create_new_user(
    user_create: UserCreate, db: AsyncSession = Depends(db_dependency)
):
    """
    Create a new user in the database.

    Parameters:
    - user_create: UserCreate - The data required to create a new user.
    - db: AsyncSession - The database session dependency.

    Returns:
    - User: The newly created user.
    """
    return await create_user(db, user_create)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User deleted successfully"},
    },
)
async def delete_current_user(
    token: str,
    db: AsyncSession = Depends(db_dependency),
):
    """
    Delete the current authenticated user.

    Parameters:
    - token: str - The JWT token of the current user.
    - db: AsyncSession - The database session dependency.

    Returns:
    - dict: A message indicating successful deletion.
    """
    await handle_user_deletion(token, db)

    return {"message": "User deleted successfully"}
