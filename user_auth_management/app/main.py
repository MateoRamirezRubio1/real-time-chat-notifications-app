from fastapi import FastAPI, Depends
from .api.v1.endpoints import user, auth
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import db_dependency
from .services.user import get_user_by_email

app = FastAPI()

# Include the routers for user and authentication endpoints
app.include_router(user.router, prefix="/api/v1/user", tags=["user"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/")
async def welcome(db: AsyncSession = Depends(db_dependency)):
    """
    Welcome endpoint to verify that the API is up and running.

    Args:
        db (AsyncSession): The asynchronous database session provided by the dependency.

    Returns:
        dict: A simple message indicating that the API is up and running.
    """
    return {"message": "Welcome to the User authentication and management API"}
