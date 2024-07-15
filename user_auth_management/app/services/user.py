from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import user as userSchemas
from ..db.models import user as userModels
from ..core.security import get_password_hash, add_token_to_revoked_list
from sqlalchemy.future import select
from starlette import status
from fastapi import HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from ..dependencies import db_dependency, verify_token


async def get_user_by_email(db: AsyncSession, user_email: str) -> userModels.User:
    """
    Retrieve a user from the database by their email.

    This function executes a query to fetch a user based on the provided email address.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_email (str): The email address of the user to be retrieved.

    Returns:
        userModels.User: The user object if found, otherwise `None`.

    Raises:
        HTTPException: Raises HTTP 500 exception for database errors.
    """
    try:
        query = select(userModels.User).where(userModels.User.email == user_email)
        result = await db.execute(query)
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error: " + str(e),
        )


async def get_current_user(
    token: str,
    db: AsyncSession = Depends(db_dependency),
) -> userModels.User:
    """
    Get the current authenticated user based on the provided token.

    This function verifies the JWT token, retrieves the user's email from the token,
    and fetches the corresponding user from the database.

    Args:
        token (str): The JWT token for authentication.
        db (AsyncSession): The asynchronous database session.

    Returns:
        userModels.User: The current authenticated user.

    Raises:
        HTTPException: Raises HTTP 401 exception if the token is invalid or the user is not found.
    """

    email = await verify_token(token, db)

    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def create_user(
    db: AsyncSession, user: userSchemas.UserCreate
) -> userModels.User:
    """
    Create a new user in the database.

    This function checks if the email is already registered, hashes the user's password,
    and then creates a new user record in the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        user (userSchemas.UserCreate): The user data for creating a new user.

    Returns:
        userModels.User: The created user object.

    Raises:
        HTTPException: Raises HTTP 400 exception if the email is already registered.
        HTTPException: Raises HTTP 500 exception for database errors.
    """
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
    """
    Delete a user from the database by their user ID.

    This function fetches the user by their ID and deletes the record from the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user to be deleted.

    Raises:
        HTTPException: Raises HTTP 500 exception for database errors.
    """
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


async def handle_user_deletion(
    token: str,
    db: AsyncSession = Depends(db_dependency),
):
    """
    Handle the deletion of the current user based on the provided token.

    This function gets the current user using the token, deletes the user from the database,
    and adds the token to the revoked list.

    Args:
        token (str): The JWT token for authentication.
        db (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException: Raises HTTP 401 exception if the user is not found.
        HTTPException: Raises HTTP 500 exception for database errors.
    """
    current_user = await get_current_user(token, db)
    await delete_user(db, current_user.pk)

    await add_token_to_revoked_list(db, token)
