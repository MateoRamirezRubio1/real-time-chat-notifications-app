from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ....services.auth import login_for_access_token
from ....schemas.auth import Token
from ....dependencies import db_dependency, verify_token
from ....dependencies import logout_for_actual_token
from ....core.config import settings

# Create a new router instance
router = APIRouter()

# Retrieve cookie name from settings
COOKIE_NAME = settings.COOKIE_NAME


@router.post(
    "/login",
    response_model=Token,
    responses={
        200: {"description": "Successful login"},
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(db_dependency),
):
    """
    Authenticate user and issue a JWT token.

    Parameters:
    - form_data: OAuth2PasswordRequestForm - The form data containing username and password.
    - db: AsyncSession - The database session dependency.

    Returns:
    - Token: The JWT token and its type.
    """
    token = await login_for_access_token(db, form_data.username, form_data.password)
    return token


@router.post(
    "/verify-token",
    responses={
        200: {
            "description": "Token is valid",
            "content": {
                "application/json": {
                    "example": {"token": "valid", "email": "example@example.com"}
                }
            },
        },
    },
)
async def verify_token_route(token: str, db: AsyncSession = Depends(db_dependency)):
    """
    Verify the validity of a JWT token.

    Parameters:
    - token: str - The JWT token to be verified.
    - db: AsyncSession - The database session dependency.

    Returns:
    - dict: A dictionary indicating if the token is valid and the associated email.
    """
    email = await verify_token(token, db)
    if email:
        return {"token": "valid", "email": email}


@router.post(
    "/logout",
    responses={
        200: {"description": "Successfully logged out"},
    },
)
async def logout(token: str, db: AsyncSession = Depends(db_dependency)):
    """
    Revoke the current JWT token.

    Parameters:
    - token: str - The JWT token to be revoked.
    - db: AsyncSession - The database session dependency.

    Returns:
    - dict: A message indicating successful logout.
    """
    await logout_for_actual_token(token, db)
    return {"message": "Successfully logged out"}
