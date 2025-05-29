from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Base schema for User properties
class UserBaseSchema(BaseModel):
    username: str

# Schema for returning user information (e.g., after creation or lookup)
# Excludes password
class UserRead(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True # This will be from_attributes in Pydantic v2
