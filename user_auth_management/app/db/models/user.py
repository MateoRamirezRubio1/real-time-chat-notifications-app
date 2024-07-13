from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = 'User'

    pk: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    userName: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password : Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)