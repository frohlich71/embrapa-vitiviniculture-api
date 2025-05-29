"""add_users_table

Revision ID: d141c5056942
Revises: b9f2adf5bdd1
Create Date: 2025-05-29 21:13:23.812489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd141c5056942'
down_revision: Union[str, None] = 'b9f2adf5bdd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # SQLModel usually creates an index for primary keys by default, so explicit ix_user_id might be redundant
    # depending on backend, but explicit ix_user_username is good.
    # If id is auto-incrementing, primary_key=True is enough. Explicit index on PK not always needed with op.create_table.
    # Let's ensure the id index is also explicitly created if that's the standard for this project.
    # op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False) # Usually not needed for PK


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_user_username'), table_name='user')
    # op.drop_index(op.f('ix_user_id'), table_name='user') # If ix_user_id was created
    op.drop_table('user')
