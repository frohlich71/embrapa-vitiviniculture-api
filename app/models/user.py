from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreateSchema(UserBase): # This is for schema validation, not directly used by CRUD yet but good for consistency
    password: str

# The UserCreate for CRUD functions will come from app.schemas.auth.UserCreate
# which has username and password. We will use User (SQLModel) for db operations.
