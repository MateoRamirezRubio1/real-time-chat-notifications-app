from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class RevokedTokenBase(BaseModel):
    token: str
    revoked_at: datetime

    class Config:
        orm_mode = True


class RevokedTokenCreate(RevokedTokenBase):
    pass


class RevokedToken(RevokedTokenBase):
    pass
