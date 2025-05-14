"""merge multiple heads

Revision ID: b9f2adf5bdd1
Revises: b9f4b811ea76, d21370a9db93
Create Date: 2025-05-06 19:56:56.812178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b9f2adf5bdd1'
down_revision: Union[str, None] = ('b9f4b811ea76', 'd21370a9db93')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
