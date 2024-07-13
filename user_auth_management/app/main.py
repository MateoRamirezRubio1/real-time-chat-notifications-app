from fastapi import FastAPI, Depends
from .api.v1.endpoints import user, auth
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import db_dependency
from .services.user import get_user_by_email

app = FastAPI()

app.include_router(user.router, prefix="/api/v1/user", tags=["user"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/")
async def welcome(db: AsyncSession = Depends(db_dependency)):
    '''
    query = select(userModel)
    result = await db.execute(query)
    userr = result.scalars().all()
    '''
    userr = await get_user_by_email(db, "string")
    return {"message": "Welcome to the User authentication and management API"}
