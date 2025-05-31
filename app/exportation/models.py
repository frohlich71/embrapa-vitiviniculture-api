from typing import Optional

from sqlmodel import Field, SQLModel


class ExportationBase(SQLModel):
    """Base model defining shared fields for importation records."""

    year: int = Field(index=True)
    country: str = Field(index=True)
    quantity_kg: float
    value: float
    path: str = Field(index=True)


class Exportation(ExportationBase, table=True):
    """Database model representing the importation table."""

    id: Optional[int] = Field(default=None, primary_key=True)


class ExportationCreate(ExportationBase):
    """Model used for creating new importation records."""

    pass


class ExportationRead(ExportationBase):
    """Model used for reading importation records."""

    id: int
