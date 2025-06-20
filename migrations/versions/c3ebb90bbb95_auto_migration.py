"""auto migration

Revision ID: c3ebb90bbb95
Revises: 52699dbcd972
Create Date: 2025-04-12 09:42:45.538142

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "c3ebb90bbb95"
down_revision: Union[str, None] = "52699dbcd972"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_processing_state", table_name="processing")
    op.create_index(
        op.f("ix_processing_cultivate"), "processing", ["cultivate"], unique=False
    )
    op.drop_column("processing", "state")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("processing", sa.Column("state", sa.VARCHAR(), nullable=False))
    op.drop_index(op.f("ix_processing_cultivate"), table_name="processing")
    op.create_index("ix_processing_state", "processing", ["state"], unique=False)
    # ### end Alembic commands ###
