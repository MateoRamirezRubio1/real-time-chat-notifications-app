from ..base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class RevokedToken(Base):
    """
    Represents the revoked tokens in the database.

    This model is used to store tokens that have been invalidated and should no longer be accepted.
    It helps to manage token revocation for security purposes.

    Attributes:
    - pk (int): The primary key of the revoked token record. Auto-incremented.
    - token (str): The revoked JWT token. Unique and indexed.
    """

    __tablename__ = "revoked_tokens"

    pk: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
