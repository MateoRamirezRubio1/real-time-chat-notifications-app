from sqlalchemy import Column, String, DateTime, Integer
from ..base import Base
from datetime import datetime


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    pk = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True)
    revoked_at = Column(DateTime, default=datetime.utcnow())
