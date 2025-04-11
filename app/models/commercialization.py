from typing import Optional

from sqlmodel import Field, SQLModel


class CommercializationBase(SQLModel):
    """Base model defining shared fields for commercialization records."""

    year: int = Field(index=True)
    product: str = Field(index=True)
    quantity_liters: float


class Commercialization(CommercializationBase, table=True):
    """Database model representing the commercialization table."""

    id: Optional[int] = Field(default=None, primary_key=True)


class CommercializationCreate(CommercializationBase):
    """Model used for creating new commercialization records."""

    pass


class CommercializationRead(CommercializationBase):
    """Model used for reading commercialization records."""

    id: int
