from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ....services.auth import login_for_access_token
from ....schemas.auth import Token
from ....dependencies import db_dependency, verify_token
from ....dependencies import logout_for_actual_token
from ....core.config import settings

router = APIRouter()

COOKIE_NAME = settings.COOKIE_NAME

@router.post(
    "/login",
    response_model=Token,
    responses={
        200: {"description": "Successful login"},
    }
)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(db_dependency),):
    """Inicia sesión y obtiene un token de acceso."""
    token = await login_for_access_token(db, form_data.username, form_data.password)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite="strict"
    )
    return token


@router.get(
    "/verify-token",
    responses={
        200: {"description": "Token is valid", "content": {"application/json": {"example": {"token": "valid", "email": "example@example.com"}}}},
    }
)
async def verify_token_route(email: str = Depends(verify_token)):
    return {"token": "valid", "email": email}

@router.post(
    "/logout",
    responses={
        200: {"description": "Successfully logged out"},
    }
)
async def logout(response: Response, logout_user: None = Depends(logout_for_actual_token)):
    response.delete_cookie(key=COOKIE_NAME, httponly=True, secure=True, samesite="strict")
    return {"message": "Successfully logged out"}
