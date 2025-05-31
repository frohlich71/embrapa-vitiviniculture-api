from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base user model with common fields"""

    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    """User table model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class UserCreate(UserBase):
    """Schema for creating a new user"""

    password: str


class UserUpdate(SQLModel):
    """Schema for updating a user"""

    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserRead(UserBase):
    """Schema for reading user data (response)"""

    id: int
    created_at: datetime
    updated_at: Optional[datetime]


class UserLogin(BaseModel):
    """Schema for user login"""

    email: str
    password: str


class Token(BaseModel):
    """Token response schema"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema"""

    email: Optional[str] = None
