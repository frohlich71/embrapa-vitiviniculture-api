"""create user table

Revision ID: b911be62d99b
Revises: 394081c68ad1
Create Date: 2025-03-31 23:11:59.609675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b911be62d99b'
down_revision: Union[str, None] = '394081c68ad1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, index=True),
        sa.Column('full_name', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_admin', sa.Boolean, default=False),
        sa.Column('hashed_password', sa.String),
    )
    op.create_index('idx_user_email', 'user', ['email'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_user_email', 'user')
    op.drop_table('user')
