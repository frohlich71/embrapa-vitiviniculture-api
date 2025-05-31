"""69ca0a20a19c

Revision ID: d4099017172d
Revises: bb602ca1d347
Create Date: 2025-04-12 09:15:47.170076

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "d4099017172d"
down_revision: Union[str, None] = "bb602ca1d347"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
