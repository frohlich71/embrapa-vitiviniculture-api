from typing import Optional

from sqlmodel import Field, SQLModel

from app.processing.constants import Category, Subcategory


class ProcessingBase(SQLModel):
    """Base model defining shared fields for processing records."""

    year: int = Field(index=True)
    cultivate: str = Field(index=True)
    quantity_kg: int
    category: Category = Field(index=True)
    subcategory: Subcategory = Field(index=True)


class Processing(ProcessingBase, table=True):
    """Database model representing the processing table."""

    id: Optional[int] = Field(default=None, primary_key=True)


class ProcessingCreate(ProcessingBase):
    """Model used for creating new procesing records."""

    pass


class ProcessingRead(ProcessingBase):
    """Model used for reading processing records."""

    id: int
