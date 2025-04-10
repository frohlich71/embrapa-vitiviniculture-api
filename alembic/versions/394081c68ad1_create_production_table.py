"""create production table

Revision ID: 394081c68ad1
Revises: 
Create Date: 2025-03-31 11:35:16.777828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '394081c68ad1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'production',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('year', sa.Integer, index=True),
        sa.Column('state', sa.String, index=True),
        sa.Column('product', sa.String),
        sa.Column('quantity_liters', sa.Float),
    )
    op.create_index('idx_production_year', 'production', ['year'])
    op.create_index('idx_production_state', 'production', ['state'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_production_state', 'production')
    op.drop_index('idx_production_year', 'production')
    op.drop_table('production')
