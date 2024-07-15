from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    This class serves as the base class for all the SQLAlchemy ORM models in the application.
    It combines the functionalities of `DeclarativeBase` for declarative table definitions
    and `AsyncAttrs` for asynchronous database operations.

    Inherits from:
    - `AsyncAttrs`: Enables the use of asynchronous methods for querying and committing.
    - `DeclarativeBase`: Provides the foundation for the declarative model definition.

    Usage:
    All SQLAlchemy models should inherit from this `Base` class.
    """

    pass
