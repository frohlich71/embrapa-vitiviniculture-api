from typing import Optional

from sqlmodel import Field, SQLModel


class ProductionBase(SQLModel):
    """Base model defining shared fields for production records."""

    year: int = Field(index=True)
    product: str = Field(index=True)
    quantity_liters: int
    category: str = Field(index=True)


class Production(ProductionBase, table=True):
    """Database model representing the production table."""

    id: Optional[int] = Field(default=None, primary_key=True)


class ProductionCreate(ProductionBase):
    """Model used for creating new production records."""

    pass


class ProductionRead(ProductionBase):
    """Model used for reading production records."""

    id: int
