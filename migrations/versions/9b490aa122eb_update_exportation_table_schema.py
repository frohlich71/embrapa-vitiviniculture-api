"""Update exportation table schema

Revision ID: 9b490aa122eb
Revises: b07d589df4f7
Create Date: 2025-05-31 01:25:35.204974

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "9b490aa122eb"
down_revision: Union[str, None] = "b07d589df4f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the exportation category enum type
    exportation_category_enum = postgresql.ENUM(
        "VINHO", "ESPUMANTES", "UVA", "SUCO", name="exportation_category"
    )
    exportation_category_enum.create(op.get_bind())

    # Add the category column (nullable first)
    op.add_column(
        "exportation", sa.Column("category", exportation_category_enum, nullable=True)
    )

    # Set default values based on existing data patterns
    # We'll set all records to 'VINHO' as default and update during data re-ingestion
    op.execute("UPDATE exportation SET category = 'VINHO'")

    # Make the column not nullable
    op.alter_column("exportation", "category", nullable=False)

    # Change data types to integer
    op.alter_column(
        "exportation",
        "quantity_kg",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "exportation",
        "value",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Integer(),
        existing_nullable=False,
    )

    # Remove the path column and its index
    op.drop_index("ix_exportation_path", table_name="exportation")
    op.drop_column("exportation", "path")

    # Create index for category
    op.create_index(
        op.f("ix_exportation_category"), "exportation", ["category"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop category index
    op.drop_index(op.f("ix_exportation_category"), table_name="exportation")

    # Add back path column
    op.add_column(
        "exportation",
        sa.Column("path", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.create_index("ix_exportation_path", "exportation", ["path"], unique=False)

    # Revert data types
    op.alter_column(
        "exportation",
        "value",
        existing_type=sa.Integer(),
        type_=sa.DOUBLE_PRECISION(precision=53),
        existing_nullable=False,
    )
    op.alter_column(
        "exportation",
        "quantity_kg",
        existing_type=sa.Integer(),
        type_=sa.DOUBLE_PRECISION(precision=53),
        existing_nullable=False,
    )

    # Drop category column
    op.drop_column("exportation", "category")

    # Drop the enum type
    exportation_category_enum = postgresql.ENUM(
        "VINHO", "ESPUMANTES", "UVA", "SUCO", name="exportation_category"
    )
    exportation_category_enum.drop(op.get_bind())
