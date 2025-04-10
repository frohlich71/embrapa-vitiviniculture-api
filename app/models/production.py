from typing import Optional
from sqlmodel import SQLModel, Field

class ProductionBase(SQLModel):
    """Base model defining shared fields for production records."""
    year: int = Field(index=True)
    state: str = Field(index=True)
    product: str
    quantity_liters: float

class Production(ProductionBase, table=True):
    """Database model representing the production table."""
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductionCreate(ProductionBase):
    """Model used for creating new production records."""
    pass

class ProductionRead(ProductionBase):
    """Model used for reading production records."""
    id: int
