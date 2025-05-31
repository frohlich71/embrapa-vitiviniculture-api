from typing import Optional

from sqlmodel import Field, SQLModel

from app.importation.constants import Category


class ImportationBase(SQLModel):
    """Base model defining shared fields for importation records."""

    year: int = Field(index=True)
    country: str = Field(index=True)
    quantity_kg: int
    category: Category = Field(index=True)


class Importation(ImportationBase, table=True):
    """Database model representing the importation table."""

    id: Optional[int] = Field(default=None, primary_key=True)


class ImportationCreate(ImportationBase):
    """Model used for creating new importation records."""

    pass


class ImportationRead(ImportationBase):
    """Model used for reading importation records."""

    id: int
