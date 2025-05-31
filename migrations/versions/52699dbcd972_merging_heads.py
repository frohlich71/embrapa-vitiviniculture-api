"""merging heads

Revision ID: 52699dbcd972
Revises: 69ca0a20a19c, d4099017172d
Create Date: 2025-04-12 09:16:43.701440

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "52699dbcd972"
down_revision: Union[str, None] = ("69ca0a20a19c", "d4099017172d")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
