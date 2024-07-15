from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Base schema for user data.

    This model defines the common fields for user data.
    """

    userName: str
    email: str
    description: str
    is_active: bool


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    This model is used for creating new users. It includes all fields from `UserBase` and adds the password field.

    Inherits from:
        UserBase: The base schema for user data.
    """

    password: str


class User(UserBase):
    """
    Schema for user details.

    This model represents the response structure for user details, including the primary key.

    Inherits from:
        UserBase: The base schema for user data.
    """

    pk: int

    class Config:
        from_attributes = True
        """
        Configures the Pydantic model to support model attributes as the data source.
        Allows attributes from SQLAlchemy models to be used directly.
        """
