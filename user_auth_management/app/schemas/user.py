from pydantic import BaseModel

class UserBase(BaseModel):
    userName: str
    email: str
    description: str
    is_active: bool

class UserCreate(UserBase):
    password: str

class User(UserBase):
    pk: int

    class Config:
        from_attributes = True