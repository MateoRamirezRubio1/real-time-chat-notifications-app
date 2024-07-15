from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    """
    Schema for authentication tokens.

    This model represents the response structure for the access token issued during login.
    """

    access_token: str
    token_type: str


class RevokedTokenBase(BaseModel):
    """
    Base schema for revoked tokens.

    This model represents the structure for revoked tokens in the database.
    """

    token: str
    revoked_at: datetime

    class Config:
        from_attributes = True


class RevokedTokenCreate(RevokedTokenBase):
    pass


class RevokedToken(RevokedTokenBase):
    pass
