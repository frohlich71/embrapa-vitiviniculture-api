from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_serializer

from app.exportation.constants import Category


class ExportationBase(SQLModel):
    """Base model defining shared fields for exportation records."""

    year: int = Field(index=True)
    country: str = Field(index=True)
    quantity_kg: int
    value: int
    category: Category = Field(index=True)

    @field_serializer('quantity_kg')
    def serialize_quantity_kg(self, value: int) -> int:
        """Ensure quantity_kg is serialized as integer."""
        return int(value)

    @field_serializer('value')
    def serialize_value(self, value: int) -> int:
        """Ensure value is serialized as integer."""
        return int(value)


class Exportation(ExportationBase, table=True):
    """Database model representing the exportation table."""

    id: Optional[int] = Field(default=None, primary_key=True)


class ExportationCreate(ExportationBase):
    """Model used for creating new exportation records."""

    pass


class ExportationRead(ExportationBase):
    """Model used for reading exportation records."""

    id: int
