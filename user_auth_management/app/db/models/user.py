from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(Base):
    """
    Represents a user in the database.

    This model is used to store user data including credentials and profile details.
    It supports user management operations like authentication and user creation.

    Attributes:
    - pk (int): The primary key of the user record. Auto-incremented.
    - userName (str): The username of the user. Unique and required.
    - email (str): The email address of the user. Unique and required.
    - password (str): The hashed password for user authentication. Required.
    - description (str): A brief description or bio of the user. Required.
    - is_active (bool): Indicates if the user account is active. Required.
    """

    __tablename__ = "users"

    pk: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    userName: Mapped[str] = mapped_column(String(length=255), nullable=False)
    email: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    description: Mapped[str] = mapped_column(String(length=255), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
